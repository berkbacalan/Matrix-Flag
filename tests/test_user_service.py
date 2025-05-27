import pytest
from app.models.user import UserCreate, User, UserRole
from app.services.user import UserService
from app.core.config import settings
from pydantic import ConfigDict
import uuid
from unittest.mock import AsyncMock, patch, Mock

@pytest.fixture
def mock_redis(mocker):
    mock = AsyncMock()
    mocker.patch('app.core.redis.get_redis', return_value=mock)
    mocker.patch('app.services.user.UserService._get_redis', return_value=mock)
    return mock

@pytest.fixture
def mock_auth(mocker):
    mocker.patch('app.core.auth.get_password_hash', return_value='hashed_password')
    mocker.patch('app.core.auth.generate_user_id', return_value='test-uuid')
    mocker.patch('app.services.user.generate_user_id', return_value='test-uuid')

@pytest.mark.asyncio
async def test_create_user(mock_redis, mock_auth):
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123",
        full_name="Test User"
    )

    user_service = UserService()
    
    created_user = await user_service.create_user(user_data)

    assert created_user.email == user_data.email
    assert created_user.full_name == user_data.full_name
    assert created_user.is_active is True
    assert created_user.role == UserRole.VIEWER
    assert created_user.id == 'test-uuid'

    mock_redis.hset.assert_called_once()
    call_args = mock_redis.hset.call_args[0]
    assert call_args[0] == "user:test-uuid"

    mock_redis.sadd.assert_called_once_with("users", "test-uuid")
    mock_redis.set.assert_called_once_with("email:test@example.com", "test-uuid")

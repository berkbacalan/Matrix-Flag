import pytest
from app.services.user import UserService


@pytest.mark.asyncio
async def test_create_user():
    service = UserService()
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
    }

    user = await service.create_user(**user_data)
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.is_active is True

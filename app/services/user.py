from typing import Optional, List
from datetime import datetime
from ..core.redis import get_redis
from ..models.user import UserInDB, UserCreate, UserUpdate, User
from ..core.auth import get_password_hash, generate_user_id

class UserService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def create_user(self, user: UserCreate) -> UserInDB:
        redis = await self._get_redis()
        user_id = generate_user_id()
        
        user_in_db = UserInDB(
            id=user_id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            hashed_password=get_password_hash(user.password)
        )
        
        await redis.hset(f"user:{user_id}", mapping=user_in_db.model_dump())
        await redis.sadd("users", user_id)
        await redis.set(f"email:{user.email}", user_id)
        
        return user_in_db

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        redis = await self._get_redis()
        user_data = await redis.hgetall(f"user:{user_id}")
        if not user_data:
            return None
        return UserInDB(**user_data)

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        redis = await self._get_redis()
        user_id = await redis.get(f"email:{email}")
        if not user_id:
            return None
        return await self.get_user_by_id(user_id)

    async def update_user(self, user_id: str, update: UserUpdate) -> Optional[UserInDB]:
        redis = await self._get_redis()
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        user_dict = user.model_dump()
        user_dict.update(update_data)
        user_dict["updated_at"] = datetime.utcnow()

        await redis.hset(f"user:{user_id}", mapping=user_dict)
        
        if "email" in update_data:
            await redis.delete(f"email:{user.email}")
            await redis.set(f"email:{update_data['email']}", user_id)
        
        return UserInDB(**user_dict)

    async def delete_user(self, user_id: str) -> bool:
        redis = await self._get_redis()
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        await redis.delete(f"user:{user_id}")
        await redis.srem("users", user_id)
        await redis.delete(f"email:{user.email}")
        return True

    async def list_users(self) -> List[User]:
        redis = await self._get_redis()
        user_ids = await redis.smembers("users")
        users = []
        for user_id in user_ids:
            user_data = await redis.hgetall(f"user:{user_id}")
            if user_data:
                user = UserInDB(**user_data)
                users.append(User(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    role=user.role,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    last_login=user.last_login
                ))
        return users

    async def update_last_login(self, user_id: str) -> None:
        redis = await self._get_redis()
        await redis.hset(f"user:{user_id}", "last_login", datetime.utcnow().isoformat())

user_service = UserService() 
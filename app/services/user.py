from typing import Optional, List
from datetime import datetime
from ..core.redis import get_redis
from ..models.user import UserInDB, UserCreate, UserUpdate, User
from ..core.auth import get_password_hash, generate_user_id
from ..core.metrics import (
    record_user_operation,
    record_redis_operation,
    update_active_users,
)
import time


class UserService:
    def __init__(self):
        self.redis = None

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def create_user(self, user: UserCreate) -> UserInDB:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user_id = generate_user_id()

            user_in_db = UserInDB(
                id=user_id,
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                hashed_password=get_password_hash(user.password),
            )

            # Convert model to dict and convert values to strings
            user_dict = user_in_db.model_dump()
            user_dict["is_active"] = str(user_dict["is_active"])
            user_dict["created_at"] = user_dict["created_at"].isoformat()
            user_dict["updated_at"] = user_dict["updated_at"].isoformat()

            # Convert None values to empty strings
            for key, value in user_dict.items():
                if value is None:
                    user_dict[key] = ""
                elif isinstance(value, datetime):
                    user_dict[key] = value.isoformat()

            await redis.hset(f"user:{user_id}", mapping=user_dict)
            await redis.sadd("users", user_id)
            await redis.set(f"email:{user.email}", user_id)

            duration = time.time() - start_time
            record_redis_operation("create_user", "success", duration)
            record_user_operation("create", "success")

            # Update active users count
            active_count = await redis.scard("users")
            update_active_users(active_count)

            return user_in_db
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("create_user", "error", duration)
            record_user_operation("create", "error")
            raise e

    async def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user_data = await redis.hgetall(f"user:{user_id}")
            if not user_data:
                duration = time.time() - start_time
                record_redis_operation("get_user", "not_found", duration)
                return None

            # Convert string values back to appropriate types
            if "is_active" in user_data:
                user_data["is_active"] = user_data["is_active"].lower() == "true"

            # Convert datetime strings back to datetime objects
            if "created_at" in user_data:
                user_data["created_at"] = datetime.fromisoformat(
                    user_data["created_at"]
                )
            if "updated_at" in user_data:
                user_data["updated_at"] = datetime.fromisoformat(
                    user_data["updated_at"]
                )
            if "last_login" in user_data and user_data["last_login"]:
                user_data["last_login"] = datetime.fromisoformat(
                    user_data["last_login"]
                )

            # Convert empty strings back to None
            for key, value in user_data.items():
                if value == "":
                    user_data[key] = None

            duration = time.time() - start_time
            record_redis_operation("get_user", "success", duration)
            return UserInDB(**user_data)
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("get_user", "error", duration)
            raise e

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user_id = await redis.get(f"email:{email}")
            if not user_id:
                duration = time.time() - start_time
                record_redis_operation(
                    "get_user_by_email", "not_found", duration)
                return None
            duration = time.time() - start_time
            record_redis_operation("get_user_by_email", "success", duration)
            return await self.get_user_by_id(user_id)
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("get_user_by_email", "error", duration)
            raise e

    async def update_user(
            self,
            user_id: str,
            update: UserUpdate) -> Optional[UserInDB]:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user = await self.get_user_by_id(user_id)
            if not user:
                duration = time.time() - start_time
                record_redis_operation("update_user", "not_found", duration)
                record_user_operation("update", "not_found")
                return None

            update_data = update.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(
                    update_data.pop("password")
                )

            user_dict = user.model_dump()
            user_dict.update(update_data)
            user_dict["updated_at"] = datetime.utcnow().isoformat()

            # Convert boolean values to strings
            if "is_active" in user_dict:
                user_dict["is_active"] = str(user_dict["is_active"])

            await redis.hset(f"user:{user_id}", mapping=user_dict)

            if "email" in update_data:
                await redis.delete(f"email:{user.email}")
                await redis.set(f"email:{update_data['email']}", user_id)

            duration = time.time() - start_time
            record_redis_operation("update_user", "success", duration)
            record_user_operation("update", "success")

            return UserInDB(**user_dict)
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("update_user", "error", duration)
            record_user_operation("update", "error")
            raise e

    async def delete_user(self, user_id: str) -> bool:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user = await self.get_user_by_id(user_id)
            if not user:
                duration = time.time() - start_time
                record_redis_operation("delete_user", "not_found", duration)
                record_user_operation("delete", "not_found")
                return False

            await redis.delete(f"user:{user_id}")
            await redis.srem("users", user_id)
            await redis.delete(f"email:{user.email}")

            duration = time.time() - start_time
            record_redis_operation("delete_user", "success", duration)
            record_user_operation("delete", "success")

            # Update active users count
            active_count = await redis.scard("users")
            update_active_users(active_count)

            return True
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("delete_user", "error", duration)
            record_user_operation("delete", "error")
            raise e

    async def list_users(self) -> List[User]:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            user_ids = await redis.smembers("users")
            users = []
            for user_id in user_ids:
                user_data = await redis.hgetall(f"user:{user_id}")
                if user_data:
                    user = UserInDB(**user_data)
                    users.append(
                        User(
                            id=user.id,
                            email=user.email,
                            full_name=user.full_name,
                            role=user.role,
                            is_active=user.is_active,
                            created_at=user.created_at,
                            updated_at=user.updated_at,
                            last_login=user.last_login,
                        )
                    )

            duration = time.time() - start_time
            record_redis_operation("list_users", "success", duration)
            return users
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("list_users", "error", duration)
            raise e

    async def update_last_login(self, user_id: str) -> None:
        start_time = time.time()
        try:
            redis = await self._get_redis()
            await redis.hset(
                f"user:{user_id}", "last_login", datetime.utcnow().isoformat()
            )

            duration = time.time() - start_time
            record_redis_operation("update_last_login", "success", duration)
        except Exception as e:
            duration = time.time() - start_time
            record_redis_operation("update_last_login", "error", duration)
            raise e


user_service = UserService()

from typing import List, Optional, Any
from datetime import datetime
from ..core.redis import get_redis
from ..models.feature_flag import FeatureFlag, FeatureFlagUpdate, WebhookEvent
import aiohttp
from ..core.config import settings


class FeatureFlagService:
    def __init__(self):
        self.redis = None
        self.webhook_urls = set()

    async def _get_redis(self):
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def create_flag(self, flag: FeatureFlag) -> FeatureFlag:
        redis = await self._get_redis()
        flag_dict = flag.model_dump()
        await redis.hset(f"flag:{flag.key}", mapping=flag_dict)
        await redis.sadd("flags", flag.key)
        return flag

    async def get_flag(self, key: str) -> Optional[FeatureFlag]:
        redis = await self._get_redis()
        flag_data = await redis.hgetall(f"flag:{key}")
        if not flag_data:
            return None
        return FeatureFlag(**flag_data)

    async def update_flag(
        self, key: str, update: FeatureFlagUpdate
    ) -> Optional[FeatureFlag]:
        redis = await self._get_redis()
        flag = await self.get_flag(key)
        if not flag:
            return None

        update_data = update.model_dump(exclude_unset=True)
        flag_dict = flag.model_dump()
        flag_dict.update(update_data)
        flag_dict["updated_at"] = datetime.utcnow()

        await redis.hset(f"flag:{key}", mapping=flag_dict)

        await self._trigger_webhook(
            "flag_updated", key, flag.value, update_data.get("value")
        )

        return FeatureFlag(**flag_dict)

    async def delete_flag(self, key: str) -> bool:
        redis = await self._get_redis()
        if not await redis.exists(f"flag:{key}"):
            return False

        await redis.delete(f"flag:{key}")
        await redis.srem("flags", key)
        await self._trigger_webhook("flag_deleted", key)
        return True

    async def list_flags(self) -> List[FeatureFlag]:
        redis = await self._get_redis()
        flag_keys = await redis.smembers("flags")
        flags = []
        for key in flag_keys:
            flag_data = await redis.hgetall(f"flag:{key}")
            if flag_data:
                flags.append(FeatureFlag(**flag_data))
        return flags

    async def add_webhook(self, url: str):
        redis = await self._get_redis()
        await redis.sadd("webhooks", url)
        self.webhook_urls.add(url)

    async def remove_webhook(self, url: str):
        redis = await self._get_redis()
        await redis.srem("webhooks", url)
        self.webhook_urls.discard(url)

    async def _trigger_webhook(
        self,
        event_type: str,
        flag_key: str,
        old_value: Any = None,
        new_value: Any = None,
    ):
        if not self.webhook_urls:
            return

        event = WebhookEvent(
            event_type=event_type,
            flag_key=flag_key,
            old_value=old_value,
            new_value=new_value,
        )

        async with aiohttp.ClientSession() as session:
            for url in self.webhook_urls:
                try:
                    async with session.post(
                        url, json=event.model_dump(), timeout=settings.WEBHOOK_TIMEOUT
                    ) as response:
                        if response.status >= 400:
                            print(f"Webhook failed for {url}: {response.status}")
                except Exception as e:
                    print(f"Webhook error for {url}: {str(e)}")


feature_flag_service = FeatureFlagService()

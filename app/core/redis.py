import redis.asyncio as redis
from ..core.config import settings

redis_pool = None


async def init_redis_pool():
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )


async def get_redis():
    """Get Redis connection"""
    return redis.from_url(settings.REDIS_URL, decode_responses=True)


async def close_redis_pool():
    if redis_pool is not None:
        await redis_pool.disconnect()

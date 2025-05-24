import redis.asyncio as redis
from .config import settings

redis_pool = None


async def init_redis_pool():
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )


async def get_redis():
    if redis_pool is None:
        await init_redis_pool()
    return redis.Redis(connection_pool=redis_pool)


async def close_redis_pool():
    if redis_pool is not None:
        await redis_pool.disconnect()

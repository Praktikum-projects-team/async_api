import functools

from db.cache.redis_cache import RedisCache
from db.redis import redis

redis_cache = RedisCache(redis)


def with_cache(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        cache_key = self.cache.get_key(*args, **kwargs)
        doc = await self.cache.get_cache(cache_key)
        if not doc:
            doc = await method(self, *args, **kwargs)
            await self.cache.set_cache(key=cache_key, value=doc)
        return doc
    return wrapper

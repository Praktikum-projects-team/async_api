import dataclasses
import functools

from db.cache.abstract_cache import AbstractCache
from db.cache.redis_cache import RedisCache, get_redis_cache
from db.redis import redis
from dataclasses import dataclass
from fastapi import Depends

redis_cache = RedisCache(redis)


@dataclass
class CacheOptions:
    ttl_in_seconds: int


class GetCache:
    def __init__(
            self,
            cache_options: CacheOptions,
    ):
        self.cache_options = cache_options
        # self.cache_provider = None

    def __call__(self, cache_provider: AbstractCache = Depends(get_redis_cache)):
        cache_provider.ttl_in_seconds = self.cache_options.ttl_in_seconds
        return cache_provider


def with_cache():
    def cache_decorator(method):
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            cache_key = self.cache.get_key(*args, **kwargs)
            doc = await self.cache.get_cache(cache_key)
            if not doc:
                doc = await method(self, *args, **kwargs)
                await self.cache.set_cache(key=cache_key, value=doc)
            return doc
        return wrapper
    return cache_decorator

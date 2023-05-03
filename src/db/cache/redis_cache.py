import logging
from functools import lru_cache
from typing import Optional, Any, Union, Iterable

import orjson
from fastapi import Depends
from redis.asyncio import Redis

from db.cache.abstract_cache import AbstractCache
from db.redis import get_redis
from models.base import BaseApiModel


class RedisCache(AbstractCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_key(self, **kwargs):
        return str(sorted(kwargs.items()))

    async def set_cache(
            self,
            /,
            key: str,
            value: Union[dict, list[dict]],
            key_extra: dict[str: Any] = None,
            ttl: int = None
    ):
        try:
            await self.redis.set(name=key, value=orjson.dumps(value), ex=ttl)
        except Exception as exc:
            logging.error(f'could not set cache {exc}')

    async def get_cache(
            self,
            /,
            key: str,
            key_extra: dict[str: Any] = None,
    ) -> Union[dict, list[dict]]:
        try:
            return orjson.loads(await self.redis.get(name=key))
        except Exception as exc:
            logging.error(f'could not get cache {exc}')


async def get_redis_cache(redis: Redis = Depends(get_redis)) -> RedisCache:
    return RedisCache(redis)

from functools import lru_cache
from typing import Optional, Any, Union, Iterable

import orjson
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.cache.abstract_cache import AbstractCache
from db.elastic import get_elastic
from db.redis import get_redis
from models.base import BaseApiModel
from models.film import Film


class RedisCache(AbstractCache):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_key(self, key_name: str, key_extra: dict[str: Any]):
        if not key_extra:
            return key_name
        return key_name + str(sorted(key_extra.items()))

    def _get_value_json(self, value: Union[BaseApiModel, list[BaseApiModel]]) -> bytes:
        if not isinstance(value, Iterable):
            return value.json()

        values = [item.json() for item in value]
        return orjson.dumps(values)

    async def set_cache(
            self,
            /,
            key_name: str,
            value: Union[BaseApiModel, list[BaseApiModel]],
            key_extra: dict[str: Any] = None,
            ttl: int = None
    ):
        key = self.get_key(key_name=key_name, key_extra=key_extra)
        value_json = self._get_value_json(value)
        await self.redis.set(name=key, value=value_json, ex=ttl)

    async def get_cache(
            self,
            /,
            key_name: str,
            key_extra: dict[str: Any] = None,
    ) -> Union[dict, list[dict]]:
        key = self.get_key(key_name=key_name, key_extra=key_extra)
        return await orjson.loads(self.redis.get(name=key))


async def get_redis_cache(redis: Redis = Depends(get_redis)) -> RedisCache:
    return RedisCache(redis)

import abc
import functools
from typing import Any, Union, Optional

from core.config import CacheTTLConfig


class AbstractCache(abc.ABC):

    def __init__(self, ttl_in_seconds: Optional[int] = None):
        self.ttl_in_seconds = ttl_in_seconds or CacheTTLConfig().default_ttl

    @abc.abstractmethod
    def get_key(self, *args, **kwargs) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def set_cache(
            self,
            /,
            key: str,
            value: Union[dict, list[dict]],
            key_extra: dict[str: Any] = None,
            ttl: int = None
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_cache(
            self,
            /,
            key: str,
            key_extra: dict[str: Any] = None,
    ) -> Union[dict, list[dict]]:
        raise NotImplementedError


def with_cache(cache: AbstractCache):
    def cache_decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = cache.get_key(*args, **kwargs)
            doc = await cache.get_cache(cache_key)
            if not doc:
                doc = await func(*args, **kwargs)
                await cache.set_cache(key=cache_key, value=doc, ttl=cache.ttl_in_seconds)
            return doc
        return wrapper
    return cache_decorator

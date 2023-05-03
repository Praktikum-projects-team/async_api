import abc
import logging
from typing import Any, Optional

from core.config import CacheTTLConfig
from db.cache.abstract_cache import AbstractCache


class AbstractFulltextSearch(abc.ABC):

    def __init__(self, cache: AbstractCache):
        self.cache = cache
        self.cache_ttl_in_seconds = CacheTTLConfig().default_ttl

    @abc.abstractmethod
    async def get_by_id_without_cache(self, index_name: str, id: Any) -> dict:
        raise NotImplementedError

    async def get_by_id(self, index_name: str, id: Any) -> dict:
        cache_key = self.cache.get_key(index_name=index_name, id=id)
        doc = await self.cache.get_cache(cache_key)
        if doc:
            logging.error('!!!!!!!!!!!!!!!! found in cache !!!!!!!!!!!!!!!!')
        if not doc:
            logging.error('!!!!!!!!!!!!!!!! not in cache !!!!!!!!!!!!!!!!')
            doc = await self.get_by_id_without_cache(index_name=index_name, id=id)
            await self.cache.set_cache(key=cache_key, value=doc, ttl=self.cache_ttl_in_seconds)
        return doc

    @abc.abstractmethod
    async def search_many_without_cache(
            self,
            index_name: str,
            query: Any,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[dict]:
        raise NotImplementedError

    async def search_many(
            self,
            index_name: str,
            query: Any,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[dict]:
        cache_key = self.cache.get_key(
            index_name=index_name, query=query, sort=sort, page_size=page_size, page_from=page_from
        )
        doc = await self.cache.get_cache(cache_key)
        if doc:
            logging.error('!!!!!!!!!!!!!!!! found in cache !!!!!!!!!!!!!!!!')
        if not doc:
            logging.error('!!!!!!!!!!!!!!!! not in cache !!!!!!!!!!!!!!!!')
            doc = await self.search_many_without_cache(
                index_name=index_name, query=query, sort=sort, page_size=page_size, page_from=page_from
            )
            await self.cache.set_cache(key=cache_key, value=doc, ttl=self.cache_ttl_in_seconds)
        return doc

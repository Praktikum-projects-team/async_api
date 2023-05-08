import abc
from typing import Any, Optional

from core.config import CacheTTLConfig
from db.cache.abstract_cache import AbstractCache, with_cache


class AbstractFulltextSearch(abc.ABC):
    cache: AbstractCache = None

    @abc.abstractmethod
    @with_cache(cache)
    async def get_by_id(self, index_name: str, id: Any) -> dict:
        raise NotImplementedError

    @abc.abstractmethod
    @with_cache(cache)
    async def search_many(
            self,
            index_name: str,
            query: Any,
            sort: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[dict]:
        raise NotImplementedError

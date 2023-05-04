from typing import Optional, Any

from elasticsearch import NotFoundError

from core.config import CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from core.base_model import OrjsonBaseModel


class BaseFulltextIndex:

    def __init__(self, searcher: AbstractFulltextSearch, index_name: str, cache_ttl: Optional[int] = None):
        self.searcher = searcher
        self.index_name = index_name
        self.searcher.cache_ttl_in_seconds = cache_ttl or CacheTTLConfig().default_ttl

    @property
    def model(self) -> type(OrjsonBaseModel):
        raise NotImplementedError

    async def _raw_get_by_id(self, id_) -> dict:
        return await self.searcher.get_by_id(index_name=self.index_name, id=id_)

    async def get_by_id(self, id_) -> Optional[OrjsonBaseModel]:
        try:
            obj = await self._raw_get_by_id(id_)
        except NotFoundError:
            return None
        return self.model(**obj)

    async def _search_by_query(
            self,
            query: Any,
            sort: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[OrjsonBaseModel]:
        objects = await self.searcher.search_many(
            index_name=self.index_name,
            query=query,
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )
        return [self.model(**obj) for obj in objects]

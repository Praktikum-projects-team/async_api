from typing import Optional, Any

from elasticsearch import NotFoundError

from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from core.base_model import OrjsonBaseModel
from models.base_model import BaseServiceModelChild


class AbstractFulltextIndex:

    def __init__(self, searcher: AbstractFulltextSearch, index_name: str):
        self.searcher = searcher
        self.index_name = index_name

    @property
    def model(self) -> type(OrjsonBaseModel):
        raise NotImplementedError

    async def _raw_get_by_id(self, id_) -> dict:
        return await self.searcher.get_by_id(index_name=self.index_name, id=id_)

    async def get_by_id(self, id_) -> Optional[BaseServiceModelChild]:
        try:
            obj = await self._raw_get_by_id(id_)
        except NotFoundError:
            return None
        return self.model(**obj)

    def _get_search_query(self, raw_query: str) -> list[dict]:
        raise NotImplementedError

    async def _search_by_query(
            self,
            query: Any,
            sort: Optional[dict] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[BaseServiceModelChild]:
        objects = await self.searcher.search_many(
            index_name=self.index_name,
            query=query,
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )
        return [self.model(**obj) for obj in objects]

    async def search(
            self,
            raw_query: str,
            sort: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[BaseServiceModelChild]:
        return await self._search_by_query(
            query=self._get_search_query(raw_query),
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )

    async def get_all(
            self,
            sort: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[BaseServiceModelChild]:
        return await self._search_by_query(
            query=None,
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )

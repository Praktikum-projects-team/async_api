import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.person import Person


class AbstractPersonIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Person):
        return Person

    def _get_search_query(self, raw_query: str) -> list[dict]:
        raise NotImplementedError

    async def search_persons(
            self,
            raw_query: str,
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Person]:
        return await self._search_by_query(
            query=self._get_search_query(raw_query),
            page_size=page_size,
            page_from=page_from,
        )

    async def get_persons(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Person]:
        raise NotImplementedError

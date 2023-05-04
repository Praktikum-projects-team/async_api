import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.film import Film


class AbstractFilmIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Film):
        return Film

    def _get_search_query(self, raw_query: str) -> list[dict]:
        raise NotImplementedError

    async def search_films(
            self,
            raw_query: str,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Film]:
        return await self._search_by_query(
            query=self._get_search_query(raw_query),
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )

    def _get_filter_query(self, raw_filter: str) -> list[dict]:
        raise NotImplementedError

    async def get_films_by_filter(
            self,
            raw_filter: str,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> [list[Film]]:  # only works with genres for now
        return await self._search_by_query(
            query=self._get_filter_query(raw_filter),
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )

    async def get_films_by_person(
            self,
            person_id: str,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> [list[Film]]:
        raise NotImplementedError

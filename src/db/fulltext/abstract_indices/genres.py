import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.genre import Genre


class AbstractGenreIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Genre):
        return Genre

    def _get_search_query(self, raw_query: str) -> list[dict]:
        raise NotImplementedError

    async def _search_genres_by_query(
            self,
            query: Any,
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Genre]:
        genres = await self.searcher.search_many(
            index_name=self.index_name,
            query=query,
            page_size=page_size,
            page_from=page_from,
        )
        return [self.model(**genre) for genre in genres]

    async def search_genres(
            self,
            raw_query: str,
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Genre]:
        return await self._search_genres_by_query(
            query=self._get_search_query(raw_query),
            page_size=page_size,
            page_from=page_from,
        )

    async def get_genres(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Genre]:
        raise NotImplementedError

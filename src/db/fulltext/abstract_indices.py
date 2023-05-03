import abc
from typing import Optional, Any

from elasticsearch import NotFoundError

from core.config import CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from models.base import BaseApiModel
from models.film import Film


class BaseFulltextIndex:

    def __init__(self, searcher: AbstractFulltextSearch, index_name: str, cache_ttl: Optional[int] = None):
        self.searcher = searcher
        self.index_name = index_name
        self.cache_ttl_in_seconds = cache_ttl or CacheTTLConfig().default_ttl

    @property
    def model(self) -> type(BaseApiModel):
        raise NotImplementedError


class AbstractFilmIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Film):
        return Film

    async def _raw_get_film_by_id(self, film_id) -> dict:
        return await self.searcher.get_by_id(index_name=self.index_name, id=film_id)

    async def _search_films_by_query(
            self,
            query: Any,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Film]:
        films = await self.searcher.search_many(
            index_name=self.index_name,
            query=query,
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )
        return [self.model(**film) for film in films]

    async def get_film_by_id(self, film_id) -> Optional[Film]:
        try:
            film = await self._raw_get_film_by_id(film_id=film_id)
        except NotFoundError:
            return None
        return self.model(**film)

    def _get_search_query(self, raw_query: str) -> list[dict]:
        raise NotImplementedError

    async def search_films(
            self,
            raw_query: str,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Film]:
        return await self._search_films_by_query(
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
    ):  # only works with genres for now
        return await self._search_films_by_query(
            query=self._get_filter_query(raw_filter),
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )

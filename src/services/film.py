from functools import lru_cache
from typing import Optional, Union

from fastapi import Depends
from orjson import orjson
from redis.asyncio import Redis

from api.v1.models_api import Page
from core import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmBase

from api.v1.models_api import Page
from db.fulltext.abstract_indices.films_index import AbstractFilmIndex
from db.fulltext.elastic.indices.films import get_elastic_film_index
from models.film import Film, FilmBase

elastic_config = config.ElasticConfig()


class FilmService:
    def __init__(self, film_index: AbstractFilmIndex):
        self.film_index = film_index

    # Заглушки для работы с Redis
    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_anything_from_cache(self):
        pass

    async def _put_anything_to_cache(self):
        pass

    # Получение одного фильма
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        return await self.film_index.get_film_by_id(film_id)

    async def get_all_films(
            self,
            sort: str,
            page: Page,
            filtering: str
    ) -> Optional[list[FilmBase]]:
        page_from = page.page_size * (page.page_number - 1)
        films = await self.film_index.get_films_by_filter(
            raw_filter=filtering,
            sort=sort,
            page_size=page.page_size,
            page_from=page_from,
        )
        return films

    async def search_film(
            self,
            page: Page,
            query: str,
            sort: str,
    ) -> Optional[list[FilmBase]]:
        page_from = page.page_size * (page.page_number - 1)
        films = await self.film_index.search_films(
            raw_query=query,
            sort=sort,
            page_size=page.page_size,
            page_from=page_from,
        )
        return films

    async def get_films_by_person(
            self,
            sort: str,
            page: Page,
            filtering: str
    ) -> Optional[list[FilmBase]]:

        query_actors = {"nested": {"path": "actors", "query": {"match": {"actors.id": filtering}}}}
        query_writers = {"nested": {"path": "writers", "query": {"match": {"writers.id": filtering}}}}
        # query_director = {"nested": {"path": "director", "query": {"match": {"director.id": filtering}}}}
        query_director = {"match": {"director.id": filtering}}
        body = {"query": {"bool": {"should": [query_actors, query_writers, query_director]}}}
        data = await self._get_anything_from_cache()
        if data:
            films = [FilmBase(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page, sort, body=body)
            await self._put_anything_to_cache()
        return films


@lru_cache()
def get_film_service(
        film_index: AbstractFilmIndex = Depends(get_elastic_film_index),
) -> FilmService:
    return FilmService(film_index)

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
    ) -> Optional[list[Film]]:
        films = await self.film_index.get_films_by_person(page, sort, body=body)
        return films


@lru_cache()
def get_film_service(
        film_index: AbstractFilmIndex = Depends(get_elastic_film_index),
) -> FilmService:
    return FilmService(film_index)

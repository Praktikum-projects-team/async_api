from functools import lru_cache
from typing import Optional

from fastapi import Depends

from core import config

from api.v1.utils import Page
from db.fulltext.abstract_indices.films_index import AbstractFilmIndex
from db.fulltext.elastic.indices.films import get_elastic_film_index
from models.film import Film, FilmBase
from services.base_service import BaseService

elastic_config = config.ElasticConfig()


class FilmService(BaseService):
    def __init__(self, index: AbstractFilmIndex):
        super().__init__(index)
        self.index = index

    async def get_all_films(
            self,
            sort: dict,
            page: Page,
            filtering: str
    ) -> Optional[list[FilmBase]]:
        films = await self.index.get_films_by_filter(
            raw_filter=filtering,
            sort=sort,
            page_size=page.page_size,
            page_from=page.page_from,
        )
        return films

    async def get_films_by_person(
            self,
            sort: dict,
            page: Page,
            filtration: str
    ) -> Optional[list[Film]]:
        films = await self.index.get_films_by_person(
            person_id=filtration,
            sort=sort,
            page_size=page.page_size,
            page_from=page.page_from,
        )
        return films


@lru_cache()
def get_film_service(
        film_index: AbstractFilmIndex = Depends(get_elastic_film_index),
) -> FilmService:
    return FilmService(film_index)

from functools import lru_cache
from typing import Optional

from fastapi import Depends

from models.genre import Genre
from core import config
from api.v1.utils import Page
from db.fulltext.abstract_indices.genres import AbstractGenreIndex
from db.fulltext.elastic.indices.genres import get_elastic_genre_index

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class GenreService:
    def __init__(self, genre_index: AbstractGenreIndex):
        self.genre_index = genre_index

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self.genre_index.get_by_id(genre_id)
        return genre

    async def get_genre_list(self, page: Page) -> Optional[list[Genre]]:
        genres = await self.genre_index.get_all(page_from=page.page_from, page_size=page.page_size)
        return genres

    async def search_genres(self, query: str, page: Page) -> Optional[list[Genre]]:
        genres = await self.genre_index.search(
            raw_query=query,
            page_size=page.page_size,
            page_from=page.page_from
        )
        return genres


@lru_cache()
def get_genre_service(
        genre_index: AbstractGenreIndex = Depends(get_elastic_genre_index),
) -> GenreService:
    return GenreService(genre_index)

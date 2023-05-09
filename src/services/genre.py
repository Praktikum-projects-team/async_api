from functools import lru_cache

from fastapi import Depends

from db.fulltext.abstract_indices.genres import AbstractGenreIndex
from db.fulltext.elastic.indices.genres import get_elastic_genre_index
from services.base_service import BaseService


class GenreService(BaseService):
    ...


@lru_cache()
def get_genre_service(
        genre_index: AbstractGenreIndex = Depends(get_elastic_genre_index),
) -> GenreService:
    return GenreService(genre_index)

from enum import Enum
from typing import Optional

from fastapi import Query

from core import config
from models.film import Film

app_config = config.AppConfig()


class FilmDetails(Film):
    pass


class Page:
    def __init__(
        self,
        page_size:  int = Query(app_config.default_page_size, ge=1),
        page_number: int = Query(1, ge=1)
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number


class FilmSortEnum(str, Enum):
    imdb_rating_asc: str = 'imdb_rating:asc'
    imdb_rating_asc_alias: str = 'imdb_rating'
    imdb_rating_desc: str = 'imdb_rating:desc'
    imdb_rating_desc_alias: str = '-imdb_rating'


class FilmSort:
    def __init__(
        self,
        sort: FilmSortEnum = Query(
            FilmSortEnum.imdb_rating_desc_alias,
            title='Sort field',
            description='Sort field (default: "-imdb_rating", sort by imdb_rating in descending order)'
        )
    ) -> None:
        if sort == FilmSortEnum.imdb_rating_asc_alias:
            sort = FilmSortEnum.imdb_rating_asc
        if sort == FilmSortEnum.imdb_rating_desc_alias:
            sort = FilmSortEnum.imdb_rating_desc
        self.sort = sort


class FilmGenreFilter:
    def __init__(
        self,
        genre_filter: Optional[str] = Query(
            None,
            title='Genre filter',
            description='Filter films by genre',
        )
    ) -> None:
        self.genre_filter = genre_filter


class FilmQuery:
    def __init__(
        self,
        query: Optional[str] = Query(
            ...,
            title='Query field',
            description='Query field (search by word in title and description field)'
        )
    ) -> None:
        self.query = query

from typing import Optional

from fastapi import Query

from core.config import AppConfig
from db.fulltext.elastic.elastic_query_formatting import FilmSortEnum, QueryFormatting


class Page:
    def __init__(
            self,
            page_size: int = Query(AppConfig().default_page_size, ge=1),
            page_number: int = Query(1, ge=1)
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number

    @property
    def page_from(self):
        return self.page_size * (self.page_number - 1)


class FilmSort:
    def __init__(
            self,
            sort: FilmSortEnum = Query(
                FilmSortEnum.imdb_rating_desc_alias,
                title='Sort field',
                description='Sort field (default: "-imdb_rating", sort by imdb_rating in descending order)'
            )
    ) -> None:
        self.sort = QueryFormatting.query_formatting_film_sort(sort)


class FilmFilter:
    def __init__(
            self,
            genre: Optional[str] = Query(
                None,
                title='Genre filter',
                description='Filter films by genre',
            ),
            person: Optional[str] = Query(
                None,
                title='Person filter',
                description='Filter films by person',
            )
    ) -> None:
        self.genre = genre
        self.person = person

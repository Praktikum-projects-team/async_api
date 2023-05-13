from enum import Enum
from http import HTTPStatus
from typing import Optional

from fastapi import Query, HTTPException

from core.config import AppConfig


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


class SortType(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


class FilmSort:
    SORTABLE_FIELDS = ('imdb_rating',)

    def __init__(
            self,
            sort: str = Query(
                '-imdb_rating',
                title='Sort field',
                description='Sort field (default: "-imdb_rating", sort by imdb_rating in descending order)'
            )
    ) -> None:
        sort_type = SortType.DESC if sort.startswith('-') else SortType.ASC
        field_name = sort.removeprefix('-')
        if field_name not in self.SORTABLE_FIELDS:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f'can not sort by {field_name}')
        self.sort = {field_name: sort_type}


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

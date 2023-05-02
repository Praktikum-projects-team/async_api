from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import Field

from core import config
from models.base import BaseApiModel
from models.film import Film, FilmPerson
from models.genre import Genre

app_config = config.AppConfig()


class FilmBaseApi(BaseApiModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


class FilmPersonApi(BaseApiModel):
    uuid: str
    full_name: str


class FilmDetailsApi(FilmBaseApi):
    description: Optional[str]
    directors: Optional[list[FilmPersonApi]] = Field(default_factory=list)
    actors: Optional[list[FilmPersonApi]] = Field(default_factory=list)
    writers: Optional[list[FilmPersonApi]] = Field(default_factory=list)
    genre: list[dict] = Field(default_factory=list)


class GenreApi(BaseApiModel):
    uuid: str
    name: str


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


class FilmFilter:
    def __init__(
        self,
        genre: Optional[str] = Query(
            None,
            title='Genre filter',
            description='Filter films by genre',
        )
    ) -> None:
        self.genre = genre


def film_to_api(film: Film) -> FilmBaseApi:
    return FilmBaseApi(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
    )


def person_to_api(person: FilmPerson) -> FilmPersonApi:
    return FilmPersonApi(
        uuid=person.id,
        full_name=person.name,
    )


def genre_to_api(genre: Genre) -> GenreApi:
    return GenreApi(
        uuid=genre.id,
        name=genre.name,
    )

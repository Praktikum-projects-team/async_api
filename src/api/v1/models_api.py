from typing import Optional

from fastapi import Query
from pydantic import Field

from core import config
from models.base import BaseApiModel
from models.film import Film, FilmPerson

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


class Page:
    def __init__(
        self,
        page_size:  int = Query(app_config.default_page_size, ge=1),
        page_number: int = Query(1, ge=1)
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number


class FilmSort:
    sort_values = [
        'imdb_rating:desc',
        '-imdb_rating',
    ]

    def __init__(
            self,
            sort: str = Query(
                'imdb_rating:desc',
                title='Sort field',
                description='Sort field (default: "-imdb_rating", sort by imdb_rating in descending order)'
            )
    ) -> None:
        if sort and sort not in self.sort_values:
            raise ValueError(f"Invalid sort field '{sort}'")
        sort = 'imdb_rating:desc'
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


def genre_to_api(genre: dict) -> dict:
    uuid = genre.pop('id')
    genre.update({'uuid': uuid})
    return genre

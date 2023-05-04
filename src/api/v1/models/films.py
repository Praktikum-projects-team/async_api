from typing import Optional
from uuid import UUID

from pydantic import Field

from api.v1.models.persons import PersonBaseApi
from api.v1.models.genres import GenreApi
from core.base_model import OrjsonBaseModel
from models.film import Film, FilmPerson


class FilmBaseApi(OrjsonBaseModel):
    uuid: UUID
    title: str
    imdb_rating: Optional[float]


class FilmDetailsApi(FilmBaseApi):
    description: Optional[str]
    directors: Optional[list[PersonBaseApi]] = Field(default_factory=list)
    actors: Optional[list[PersonBaseApi]] = Field(default_factory=list)
    writers: Optional[list[PersonBaseApi]] = Field(default_factory=list)
    genre: list[GenreApi] = Field(default_factory=list)


def film_to_api(film: Film) -> FilmBaseApi:
    return FilmBaseApi(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
    )


def person_to_api(person: FilmPerson) -> PersonBaseApi:
    return PersonBaseApi(
        uuid=person.id,
        full_name=person.name,
    )

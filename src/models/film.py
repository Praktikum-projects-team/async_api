from typing import Optional

from pydantic import Field

from models.base import BaseApiModel


class FilmBase(BaseApiModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class FilmPerson(BaseApiModel):
    id: str
    name: str


class Film(FilmBase):
    description: Optional[str]
    directors: Optional[list[FilmPerson]] = Field(default_factory=list)
    actors: Optional[list[FilmPerson]] = Field(default_factory=list)
    writers: Optional[list[FilmPerson]] = Field(default_factory=list)
    genre: list[str] = Field(default_factory=list)

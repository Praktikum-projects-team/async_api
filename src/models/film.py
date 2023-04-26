from pydantic import UUID4, Field
from base import BaseApiModel
from genre import Genre
from person import PersonBase
from typing import Optional


class FilmBase(BaseApiModel):
    uuid: UUID4
    title: str
    imdb_rating: Optional[float]


class Film(FilmBase):
    description: Optional[str]
    directors: Optional[list[PersonBase]] = Field(default_factory=list)
    actors: Optional[list[PersonBase]] = Field(default_factory=list)
    writers: Optional[list[PersonBase]] = Field(default_factory=list)
    genre: list[Genre]

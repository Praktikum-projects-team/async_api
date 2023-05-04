from typing import Optional

from pydantic import Field

from core.base_model import OrjsonBaseModel
from models.genre import Genre


class FilmBase(OrjsonBaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class FilmPerson(OrjsonBaseModel):
    id: str
    name: str


class Film(FilmBase):
    description: Optional[str]
    directors: Optional[list[FilmPerson]] = Field(default_factory=list)
    actors: Optional[list[FilmPerson]] = Field(default_factory=list)
    writers: Optional[list[FilmPerson]] = Field(default_factory=list)
    genre: list[Genre] = Field(default_factory=list)

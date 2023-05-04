from typing import Optional

from pydantic import Field, UUID4

from models.base import BaseApiModel


class PersonFilms(BaseApiModel):
    role: list[str]
    id: str


class Person(BaseApiModel):
    id: str
    full_name: str
    films: list[PersonFilms] = Field(default_factory=list)

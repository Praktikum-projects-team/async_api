from typing import Optional

from pydantic import Field, UUID4

from models.base import BaseApiModel


class PersonFilms:
    roles: list[str]
    id: str


class Person(BaseApiModel):
    id: str
    full_name: str
    films: Optional[list[PersonFilms]] = Field(default_factory=list)

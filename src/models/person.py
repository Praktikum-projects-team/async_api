from typing import Optional

from pydantic import Field, UUID4

from models.base import BaseApiModel


class PersonFilms:
    roles: list[str]
    uuid: UUID4


class PersonBase(BaseApiModel):
    uuid: UUID4
    full_name: str
    films: Optional[list[PersonFilms]] = Field(default_factory=list)

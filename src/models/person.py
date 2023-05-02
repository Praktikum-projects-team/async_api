from pydantic import UUID4, Field
from models.base import BaseApiModel
from typing import Optional


class PersonFilms(BaseApiModel):
    roles: list[str]
    uuid: UUID4


class PersonBase(BaseApiModel):
    uuid: UUID4
    full_name: str
    films: Optional[list[PersonFilms]] = Field(default_factory=list)

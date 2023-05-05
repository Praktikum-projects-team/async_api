from uuid import UUID

from pydantic import Field

from core.base_model import OrjsonBaseModel


class PersonFilms(OrjsonBaseModel):
    role: list[str]
    id: UUID


class Person(OrjsonBaseModel):
    id: UUID
    full_name: str
    films: list[PersonFilms] = Field(default_factory=list)

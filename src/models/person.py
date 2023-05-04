from pydantic import Field

from core.base_model import OrjsonBaseModel


class PersonFilms(OrjsonBaseModel):
    role: list[str]
    id: str


class Person(OrjsonBaseModel):
    id: str
    full_name: str
    films: list[PersonFilms] = Field(default_factory=list)

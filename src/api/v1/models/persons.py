from typing import Optional
from uuid import UUID

from pydantic import Field

from models.base import BaseApiModel
from models.person import Person


class PersonBaseApi(BaseApiModel):
    uuid: UUID
    full_name: str


class PersonFilmsApi(BaseApiModel):
    role: list[str]
    uuid: UUID


class PersonApi(PersonBaseApi):
    films: Optional[list[PersonFilmsApi]] = Field(default_factory=list)


def person_to_api_detail(person: Person) -> PersonApi:
    person_films = []
    for film in person.films:
        person_films.append(PersonFilmsApi(role=film.role, uuid=film.id))
    return PersonApi(
        uuid=person.id,
        full_name=person.full_name,
        films=person_films
    )



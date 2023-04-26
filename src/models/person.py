from pydantic import UUID4
from base import BaseApiModel


class PersonFilms:
    roles: list[str]
    uuid: UUID4


class PersonBase(BaseApiModel):
    uuid: UUID4
    full_name: str
    films: list[PersonFilms]

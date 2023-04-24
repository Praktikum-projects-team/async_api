import orjson
from pydantic import BaseModel, UUID4
from film import FilmBase


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class PersonBase(BaseModel):
    id: UUID4
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(PersonBase):
    role: list[str]
    films: list[FilmBase]



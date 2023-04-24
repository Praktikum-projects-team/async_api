import orjson
from pydantic import BaseModel, UUID4
from datetime import date
from genre import Genre
from person import PersonBase


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FilmBase(BaseModel):
    id: UUID4
    title: str
    description: str
    creation_date: date
    imdb_rating: float

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(FilmBase):
    directors: list[PersonBase] = []
    actors: list[PersonBase] = []
    writers: list[PersonBase] = []
    genre: list[Genre] = []




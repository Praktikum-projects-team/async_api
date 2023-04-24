import orjson
from pydantic import BaseModel, UUID4


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: UUID4
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

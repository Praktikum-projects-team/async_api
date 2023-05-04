from uuid import UUID

from models.base import BaseApiModel
from models.genre import Genre


class GenreApi(BaseApiModel):
    uuid: UUID
    name: str


def genre_to_api(genre: Genre) -> GenreApi:
    return GenreApi(
        uuid=genre.id,
        name=genre.name,
    )
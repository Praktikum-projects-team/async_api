from uuid import UUID

from core.base_model import OrjsonBaseModel
from models.genre import Genre


class GenreApi(OrjsonBaseModel):
    uuid: UUID
    name: str


def genre_to_api(genre: Genre) -> GenreApi:
    return GenreApi(
        uuid=genre.id,
        name=genre.name,
    )
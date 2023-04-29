from pydantic import UUID4

from models.base import BaseApiModel


class Genre(BaseApiModel):
    uuid: UUID4
    name: str

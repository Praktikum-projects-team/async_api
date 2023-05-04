from uuid import UUID

from core.base_model import OrjsonBaseModel


class Genre(OrjsonBaseModel):
    id: UUID
    name: str

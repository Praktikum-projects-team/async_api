from pydantic import Field

from models.base import BaseApiModel


# Классы для фильтрации фильмов по жанрам
class EsFilterGenreValue(BaseApiModel):
    value: str = Field('')
    boost: float = 1.0


class EsFilterGenreField(BaseApiModel):
    genre: EsFilterGenreValue = Field(EsFilterGenreValue())


class EsFilterTermGenre(BaseApiModel):
    term: EsFilterGenreField = Field(EsFilterGenreField())


class EsFilterGenre(BaseApiModel):
    query: EsFilterTermGenre = Field(EsFilterTermGenre())

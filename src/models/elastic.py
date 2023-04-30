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


# Классы для поиска фильмов
class EsQuerySearchParameters(BaseApiModel):
    query: str = Field('')
    search_fields: list[str] = Field(['title', 'description'])


class EsQuerySearchType(BaseApiModel):
    multi_match: EsQuerySearchParameters = Field(EsQuerySearchParameters())


class EsQuery(BaseApiModel):
    query: EsQuerySearchType = Field(EsQuerySearchType())

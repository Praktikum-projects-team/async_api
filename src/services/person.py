from functools import lru_cache

from fastapi import Depends

from db.fulltext.abstract_indices.persons import AbstractPersonIndex
from db.fulltext.elastic.indices.persons import get_elastic_person_index
from services.base_service import BaseService


class PersonService(BaseService):
    ...


@lru_cache()
def get_person_service(
        person_index: AbstractPersonIndex = Depends(get_elastic_person_index),
) -> PersonService:
    return PersonService(person_index)

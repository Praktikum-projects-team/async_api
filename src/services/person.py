from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.fulltext.abstract_indices.persons import AbstractPersonIndex
from db.fulltext.elastic.indices.persons import get_elastic_person_index
from db.redis import get_redis
from models.person import Person, PersonFilms
from core import config
from api.v1.models_api import Page

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class PersonService:
    def __init__(self, person_index: AbstractPersonIndex):
        self.person_index = person_index

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self.person_index.get_person_by_id(person_id)
        return person

    async def get_persons_list(self, page: Page) -> Optional[list[Person]]:
        from_page = page.page_size * (page.page_number - 1)
        persons = await self.person_index.get_persons(page_from=from_page, page_size=page.page_size)
        return persons

    async def search_persons(self, query: str, page: Page) -> Optional[list[Person]]:
        from_page = page.page_size * (page.page_number - 1)
        persons = await self.person_index.search_persons(raw_query=query, page_size=page.page_size, page_from=from_page)
        return persons


@lru_cache()
def get_person_service(
        person_index: AbstractPersonIndex = Depends(get_elastic_person_index),
) -> PersonService:
    return PersonService(person_index)


from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonBase, PersonFilms
from core import config
from api.v1.models_api import Page

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[PersonBase]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def get_persons_list(self, page: Page) -> Optional[list[PersonBase]]:
        body = {"query": {"match_all": {}}}
        persons = await self._persons_from_cache()
        if not persons:
            persons = await self._get_persons_from_elastic(body, page)
            if not persons:
                return None
            await self._put_persons_to_cache(persons)
        return persons

    async def search_persons(self, query: str, page: Page) -> Optional[list[PersonBase]]:
        body = {"query": {"bool": {"must": [{"multi_match": {"query": query, "fields": ["full_name"]}}]}}}
        persons = await self._persons_from_cache()
        if not persons:
            persons = await self._get_persons_from_elastic(body, page)
            if not persons:
                return None
            await self._put_persons_to_cache(persons)
        return persons

    async def _get_person_from_elastic(self, person_id: str) -> Optional[PersonBase]:
        try:
            doc = await self.elastic.get(elastic_config.index_person, person_id)
        except NotFoundError:
            return None
        person_films = [PersonFilms(roles=film['role'], id=film['id']) for film in doc['_source']['films']]
        return PersonBase(id=doc['_source']['id'], full_name=doc['_source']['full_name'], films=person_films)

    async def _get_persons_from_elastic(self, body, page) -> Optional[list[PersonBase]]:
        try:
            from_ = page.page_size * (page.page_number - 1)
            docs = await self.elastic.search(index=elastic_config.index_person, body=body, from_=from_)
            persons = []
            for doc in docs['hits']['hits']:
                person_films = [PersonFilms(roles=film['role'], id=film['id']) for film in doc['_source']['films']]
                persons.append(
                    PersonBase(id=doc['_source']['id'], full_name=doc['_source']['full_name'], films=person_films))
        except NotFoundError:
            return None
        return persons

    async def _person_from_cache(self, person_id: str) -> Optional[PersonBase]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = PersonBase.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: PersonBase):
        await self.redis.set(str(person.id), person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _persons_from_cache(self) -> Optional[list[PersonBase]]:
        pass

    async def _put_persons_to_cache(self, persons: list[PersonBase]):
        pass


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)

from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from src.models.person import PersonBase

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


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
            await self._put_genre_to_cache(person)
        return person

    # Write func for returning list of all persons
    async def get_list(self) -> Optional[list[PersonBase]]:
        pass

    async def _get_person_from_elastic(self, person_id: str) -> Optional[PersonBase]:
        try:
            doc = await self.elastic.get('person', person_id)
        except NotFoundError:
            return None
        return PersonBase(**doc['_source'])

    async def _person_from_cache(self, person_id: str) -> Optional[PersonBase]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = PersonBase.parse_raw(data)
        return person

    async def _put_genre_to_cache(self, person: PersonBase):
        await self.redis.set(person.id, person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)

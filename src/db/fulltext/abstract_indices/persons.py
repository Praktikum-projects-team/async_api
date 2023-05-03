import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.person import Person


class AbstractPersonIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Person):
        return Person

    async def _raw_get_person_by_id(self, person_id) -> dict:
        return await self.searcher.get_by_id(index_name=self.index_name, id=person_id)

    async def get_person_by_id(self, person_id) -> Optional[Person]:
        try:
            person = await self._raw_get_person_by_id(person_id=person_id)
        except NotFoundError:
            return None
        return self.model(**person)

    async def _search_persons_by_query(
            self,
            query: Any,
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[Person]:
        persons = await self.searcher.search_many(
            index_name=self.index_name,
            query=query,
            page_size=page_size,
            page_from=page_from,
        )
        return [self.model(**person) for person in persons]

    async def get_persons(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Person]:
        raise NotImplementedError
from typing import Optional

from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.persons import AbstractPersonIndex
from db.fulltext.elastic.elastic_fulltext_search import get_elastic_fulltext_search
from models.person import Person


class ESPersonIndex(AbstractPersonIndex):

    def _get_search_query(self, raw_query: str) -> list[dict]:
        if not raw_query:
            return None
        return [{"multi_match": {"query": raw_query, "fields": ["title", "description"]}}]

    def _get_filter_query(self, raw_filter: str) -> list[dict]:
        if not raw_filter:
            return None
        return [{"nested": {"path": "genre", "query": {"match": {"genre.id": raw_filter}}}}]

    async def get_persons(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Person]:
        query = [{"multi_match": {"query": raw_query, "fields": ["full_name"]}}]
        persons = await self._search_persons_by_query(
            query=query,
            page_size=page_size,
            page_from=page_from,
        )
        return persons

def get_elastic_person_index(
        es_searcher: AbstractFulltextSearch = Depends(get_elastic_fulltext_search)
) -> ESPersonIndex:
    return ESPersonIndex(searcher=es_searcher, index_name=ElasticConfig().index_person, cache_ttl=CacheTTLConfig().persons_ttl)
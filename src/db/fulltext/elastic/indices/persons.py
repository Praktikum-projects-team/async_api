from typing import Optional

from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.persons import AbstractPersonIndex
from db.fulltext.elastic.elastic_fulltext_search import get_elastic_fulltext_search
from models.person import Person


class ESPersonIndex(AbstractPersonIndex):

    async def get_persons(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Person]:
        query = [{"multi_match": {"query": raw_query, "fields": ["full_name"]}}] if raw_query else None
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
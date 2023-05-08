from typing import Optional

from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.persons import AbstractPersonIndex
from db.fulltext.elastic.elastic_fulltext_search import GetElasticFulltextSearch
from models.person import Person


class ESPersonIndex(AbstractPersonIndex):

    def _get_search_query(self, raw_query: str) -> list[dict]:
        if not raw_query:
            return None
        return [{"multi_match": {"query": raw_query, "fields": ["full_name"]}}]


def get_elastic_person_index(
        es_searcher: AbstractFulltextSearch = Depends(GetElasticFulltextSearch(CacheTTLConfig().persons_ttl))
) -> ESPersonIndex:
    return ESPersonIndex(searcher=es_searcher, index_name=ElasticConfig().index_person)

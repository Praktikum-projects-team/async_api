from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.genres import AbstractGenreIndex
from db.fulltext.elastic.elastic_fulltext_search import GetElasticFulltextSearch


class ESGenreIndex(AbstractGenreIndex):

    def _get_search_query(self, raw_query: str) -> list[dict]:
        if not raw_query:
            return None
        return [{"multi_match": {"query": raw_query, "fields": ["name"]}}]


def get_elastic_genre_index(
        es_searcher: AbstractFulltextSearch = Depends(GetElasticFulltextSearch(CacheTTLConfig().genres_ttl))
) -> ESGenreIndex:
    return ESGenreIndex(searcher=es_searcher, index_name=ElasticConfig().index_genre)

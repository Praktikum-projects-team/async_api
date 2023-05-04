from typing import Optional

from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.genres import AbstractGenreIndex
from db.fulltext.elastic.elastic_fulltext_search import get_elastic_fulltext_search
from models.genre import Genre


class ESGenreIndex(AbstractGenreIndex):

    def _get_search_query(self, raw_query: str) -> list[dict]:
        if not raw_query:
            return None
        return [{"multi_match": {"query": raw_query, "fields": ["name"]}}]

    async def get_genres(
            self,
            raw_query: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[Genre]:
        query = self._get_search_query(raw_query)
        genres = await self._search_by_query(
            query=query,
            page_size=page_size,
            page_from=page_from,
        )
        return genres


def get_elastic_genre_index(
        es_searcher: AbstractFulltextSearch = Depends(get_elastic_fulltext_search)
) -> ESGenreIndex:
    return ESGenreIndex(searcher=es_searcher, index_name=ElasticConfig().index_genre,
                        cache_ttl=CacheTTLConfig().genres_ttl)

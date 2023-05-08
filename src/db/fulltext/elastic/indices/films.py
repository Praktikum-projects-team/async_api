from typing import Optional

from fastapi import Depends

from core.config import ElasticConfig, CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from db.fulltext.abstract_indices.films_index import AbstractFilmIndex
from db.fulltext.elastic.elastic_fulltext_search import get_elastic_fulltext_search
from models.film import Film


class ESFilmIndex(AbstractFilmIndex):

    def _get_search_query(self, raw_query: str) -> list[dict]:
        if not raw_query:
            return None
        return [{"multi_match": {"query": raw_query, "fields": ["title", "description"]}}]

    def _get_filter_query(self, raw_filter: str) -> list[dict]:
        if not raw_filter:
            return None
        return [{"nested": {"path": "genre", "query": {"match": {"genre.id": raw_filter}}}}]

    async def get_films_by_person(
            self,
            person_id: str,
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> [list[Film]]:
        query_actors = {"nested": {"path": "actors", "query": {"match": {"actors.id": person_id}}}}
        query_writers = {"nested": {"path": "writers", "query": {"match": {"writers.id": person_id}}}}
        query_director = {"match": {"director.id": person_id}}
        query = {"should": [query_actors, query_writers, query_director]}
        return await self._search_by_query(
            query=query,
            sort=sort,
            page_size=page_size,
            page_from=page_from,
        )


def get_elastic_film_index(
        es_searcher: AbstractFulltextSearch = Depends(get_elastic_fulltext_search)
) -> ESFilmIndex:
    return ESFilmIndex(
        searcher=es_searcher, index_name=ElasticConfig().index_movies, cache_ttl=CacheTTLConfig().movies_ttl
    )

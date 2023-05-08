from typing import Any, Union, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache.abstract_cache import AbstractCache, with_cache
from db.cache.redis_cache import get_redis_cache
from db.elastic import get_elastic
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch


class ElasticFulltextSearch(AbstractFulltextSearch):
    cache: AbstractCache = Depends(get_redis_cache)

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    @with_cache(cache)
    async def get_by_id(self, index_name: str, id: Any) -> dict:
        doc = await self.elastic.get(index=index_name, id=id)
        return doc['_source']

    @with_cache(cache)
    async def search_many(
            self,
            index_name: str,
            query: Union[list[dict], str],
            sort: Optional[str] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[dict]:

        body = {"query": {"bool": {"must": query}}} if query else None
        if type(query) == dict:
            body = {"query": {"bool": query}}

        docs = await self.elastic.search(
            index=index_name,
            sort=sort,
            size=page_size,
            from_=page_from,
            body=body,
        )
        return [doc['_source'] for doc in docs['hits']['hits']]


def get_elastic_fulltext_search(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticFulltextSearch:
    return ElasticFulltextSearch(elastic)

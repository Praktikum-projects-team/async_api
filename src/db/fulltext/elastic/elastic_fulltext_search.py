from typing import Any, Union, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache.cache_decorator import with_cache, GetCache, CacheOptions
from db.cache.abstract_cache import AbstractCache
from db.elastic import get_elastic
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch


class ElasticFulltextSearch(AbstractFulltextSearch):
    def __init__(self, elastic: AsyncElasticsearch, cache: AbstractCache):
        self.elastic = elastic
        self.cache = cache

    @with_cache()
    async def get_by_id(self, index_name: str, id: Any) -> dict:
        doc = await self.elastic.get(index=index_name, id=id)
        return doc['_source']

    @with_cache()
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
        cache: AbstractCache = Depends(GetCache(cache_options=CacheOptions(ttl_in_seconds=10)))
) -> ElasticFulltextSearch:
    return ElasticFulltextSearch(elastic, cache)

from typing import Any, Union, Optional

import backoff
from elasticsearch import AsyncElasticsearch, TransportError
from fastapi import Depends

from db.cache.cache_decorator import with_cache
from api.v1.utils import SortType
from db.cache.abstract_cache import AbstractCache
from db.cache.redis_cache import get_redis_cache
from db.elastic import get_elastic
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch


class ElasticFulltextSearch(AbstractFulltextSearch):
    def __init__(self, elastic: AsyncElasticsearch, cache: AbstractCache):
        self.elastic = elastic
        self.cache = cache

    @with_cache
    @backoff.on_exception(
        backoff.expo,
        TransportError,
        max_tries=5,
    )
    async def get_by_id(self, index_name: str, id: Any) -> dict:
        doc = await self.elastic.get(index=index_name, id=id)
        return doc['_source']

    @with_cache
    @backoff.on_exception(
        backoff.expo,
        TransportError,
        max_tries=5,
    )
    async def search_many(
            self,
            index_name: str,
            query: Union[list[dict], str],
            sort: Optional[dict] = None,
            page_size: Optional[int] = None,
            page_from: Optional[int] = None,
    ) -> list[dict]:

        body = {"query": {"bool": {"must": query}}} if query else None
        if type(query) == dict:
            body = {"query": {"bool": query}}

        sort_type = await self.format_sorting(sort)

        docs = await self.elastic.search(
            index=index_name,
            sort=sort_type,
            size=page_size,
            from_=page_from,
            body=body,
        )
        return [doc['_source'] for doc in docs['hits']['hits']]

    @staticmethod
    async def format_sorting(sort: dict[str: SortType]) -> Optional[Any]:
        if not sort:
            return None
        field, sort_type = sort.popitem()
        return field + ':' + sort_type.value


class GetElasticFulltextSearch:
    def __init__(
            self,
            ttl_in_seconds: int,
    ):
        self.ttl_in_seconds = ttl_in_seconds

    def __call__(
            self,
            elastic: AsyncElasticsearch = Depends(get_elastic),
            cache: AbstractCache = Depends(get_redis_cache)
    ) -> ElasticFulltextSearch:
        cache.ttl_in_seconds = self.ttl_in_seconds
        return ElasticFulltextSearch(elastic, cache)

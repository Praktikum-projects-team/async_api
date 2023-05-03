from typing import Any, Union, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache.abstract_cache import AbstractCache
from db.cache.redis_cache import get_redis_cache
from db.elastic import get_elastic
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch


class ElasticFulltextSearch(AbstractFulltextSearch):

    def __init__(self, elastic: AsyncElasticsearch, cache: AbstractCache):
        super().__init__(cache)
        self.elastic = elastic

    async def get_by_id_without_cache(self, index_name: str, id: Any) -> dict:
        doc = await self.elastic.get(index=index_name, id=id)
        return doc['_source']

    async def search_many_without_cache(
            self,
            index_name: str,
            query: Union[list[dict], str],
            sort: Optional[str],
            page_size: Optional[int],
            page_from: Optional[int],
    ) -> list[dict]:
        body = {"query": {"bool": {"must": query}}} if query else None

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
        cache: AbstractCache = Depends(get_redis_cache),
) -> ElasticFulltextSearch:
    return ElasticFulltextSearch(elastic, cache)

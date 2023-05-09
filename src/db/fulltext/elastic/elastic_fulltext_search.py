from typing import Any, Union, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from api.v1.utils import SortType
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


def get_elastic_fulltext_search(
        elastic: AsyncElasticsearch = Depends(get_elastic),
        cache: AbstractCache = Depends(get_redis_cache),
) -> ElasticFulltextSearch:
    return ElasticFulltextSearch(elastic, cache)

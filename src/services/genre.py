from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from core import config
from api.v1.models_api import Page

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_genre_list(self, page: Page) -> Optional[list[Genre]]:
        body = {"query": {"match_all": {}}}
        genres = await self._genres_from_cache()
        if not genres:
            genres = await self._get_genres_from_elastic(body, page)
            if not genres:
                return None
            await self._put_genres_to_cache(genres)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(elastic_config.index_genre, genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _get_genres_from_elastic(self, body, page: Page) -> Optional[list[Genre]]:
        try:
            from_ = page.page_size * (page.page_number - 1)
            docs = await self.elastic.search(index=elastic_config.index_genre, size=page.page_size,
                                             from_=from_, body=body)
            genres = [Genre(**doc['_source']) for doc in docs['hits']['hits']]
        except NotFoundError:
            return None
        return genres

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(str(genre.id), genre.json(), GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def _genres_from_cache(self) -> Optional[list[Genre]]:
        pass

    async def _put_genres_to_cache(self, genres: list[Genre]):
        pass


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)

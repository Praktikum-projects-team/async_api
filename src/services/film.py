from functools import lru_cache
from typing import Optional, Union

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from orjson import orjson
from redis.asyncio import Redis

from api.v1.models_api import Page
from core import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmBase

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # Заглушки для работы с Redis
    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_anything_from_cache(self):
        pass

    async def _put_anything_to_cache(self):
        pass

    # Получение одного фильма
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    # Получение списка фильмов
    async def get_all_films(
            self,
            sort: str,
            page: Page,
            filtering: str
    ) -> Optional[list[FilmBase]]:

        query = {"nested": {"path": "genre", "query": {"match": {"genre.id": filtering}}}}
        body = {"query": {"bool": {"must": [query]}}}

        data = await self._get_anything_from_cache()
        if data:
            films = [FilmBase(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page, sort, body=body)
            await self._put_anything_to_cache()
        return films

    # Поиск фильмов
    async def search_film(
            self,
            page: Page,
            query: str,
            sort: str,
    ) -> Optional[list[FilmBase]]:
        body = {"query": {"bool": {"must": [{"multi_match": {"query": query, "fields": ["title", "description"]}}]}}}

        data = await self._get_anything_from_cache()
        if data:
            films = [FilmBase(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page, sort, body=body)
            await self._put_anything_to_cache()
        return films

    # Запросы в Elasticsearch
    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(elastic_config.index_movies, film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _get_films_from_elastic(
            self,
            page: Page,
            sort: str = None,
            body: Union[str, dict] = None,
    ) -> Optional[list[Film]]:
        from_ = page.page_size * (page.page_number - 1)

        docs = await self.elastic.search(
            index=elastic_config.index_movies,
            sort=sort,
            size=page.page_size,
            from_=from_,
            body=body
        )

        films = [Film(**doc['_source']) for doc in docs['hits']['hits']]
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)

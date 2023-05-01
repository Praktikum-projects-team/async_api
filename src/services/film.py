from functools import lru_cache
from typing import Optional, Union

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from orjson import orjson
from redis.asyncio import Redis

from core import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.elastic import EsFilterGenre
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

elastic_config = config.ElasticConfig()


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

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

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(elastic_config.index_movies, film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)

    # Получение списка фильмов
    async def get_all_films(
            self,
            sort: str,
            page_size: int,
            page_number: int,
            genre_filter: str
    ) -> Optional[list[Film]]:

        if genre_filter:
            filter_ = EsFilterGenre()
            filter_.query.term.genre.value = genre_filter
            genre_filter = filter_.json()

        data = await self._get_anything_from_cache()
        if data:
            films = [Film(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page_size, page_number, sort, body=genre_filter)
            await self._put_anything_to_cache()
        return films

    async def _get_films_from_elastic(
            self,
            page_size: int,
            page_number: int,
            sort: str = None,
            body: Union[str, dict] = None,
    ) -> Optional[list[Film]]:
        from_ = page_size * (page_number - 1)

        docs = await self.elastic.search(
            index=elastic_config.index_movies,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body
        )

        films = [Film(**doc['_source']) for doc in docs['hits']['hits']]
        return films

    # Поиск фильмов
    async def search_film(
            self,
            page_size: int,
            page_number: int,
            query: str
    ) -> Optional[list[Film]]:
        body = {"query": {"bool": {"must": [{"multi_match": {"query": query, "fields": ["title", "description"]}}]}}}

        data = await self._get_anything_from_cache()
        if data:
            films = [Film(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page_size, page_number, body=body)
            await self._put_anything_to_cache()
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)

from asyncio import sleep

import pytest

from tests.functional.testdata.genres import get_genres_data, get_genre_uuid
from tests.functional.utils.constants import CACHE_TTL, DEFAULT_PAGE_SIZE, EsIndex, Sort
from tests.functional.utils.routes import GENRES_URL
import logging


class TestGenre:

    @pytest.mark.asyncio
    async def test_one_genre(self, es_write_data, make_get_request):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        await es_write_data(EsIndex.GENRE, genre)
        response = await make_get_request(f'{GENRES_URL}/{genre_uuid}')

        assert response.status == 200, 'Wrong status code'
        assert 'uuid' in response.body, 'No uuid in response'
        assert 'name' in response.body, 'No genre name in response'
        assert response.body['uuid'] == genre_uuid, 'Wrong uuid in response'
        assert response.body['name'] == genre[0]['name'], 'Wrong genre name in response'

    @pytest.mark.asyncio
    async def test_one_genre_not_in_es(self, es_write_data, make_get_request):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        wrong_uuid = f'{genre_uuid}abc'
        await es_write_data(EsIndex.GENRE, genre)
        response = await make_get_request(f'{GENRES_URL}/{wrong_uuid}')

        assert response.status == 404, 'Wrong status code'
        assert response.body['detail'] == 'genre not found', 'Wrong error message'


class TestGenres:
    @pytest.mark.asyncio
    async def test_all_genre_default_page(self, es_write_data, make_get_request):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL)

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == DEFAULT_PAGE_SIZE, 'Wrong page size in response'
        for genre in response.body:
            assert 'uuid' in genre, 'No uuid in response'
            assert 'name' in genre, 'No genre name in response'

    @pytest.mark.parametrize('page_size', [1, 15, 19, 20, 21, '10'])
    @pytest.mark.asyncio
    async def test_all_genres_page_size(self, es_write_data, make_get_request, page_size):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_size': page_size})

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == int(page_size), 'Wrong page size in response'




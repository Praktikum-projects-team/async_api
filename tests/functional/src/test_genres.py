from asyncio import sleep
from http import HTTPStatus

import pytest

from tests.functional.testdata.genres import get_genres_data, get_genre_uuid
from tests.functional.utils.constants import CACHE_TTL, DEFAULT_PAGE_SIZE, EsIndex
from tests.functional.utils.routes import GENRES_URL
import logging

pytestmark = pytest.mark.asyncio


class TestGenre:

    async def test_one_genre(self, es_write_data, make_get_request):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        await es_write_data(EsIndex.GENRE, genre)
        response = await make_get_request(f'{GENRES_URL}/{genre_uuid}')

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert 'uuid' in response.body, 'No uuid in response'
        assert 'name' in response.body, 'No genre name in response'
        assert response.body['uuid'] == genre_uuid, 'Wrong uuid in response'
        assert response.body['name'] == genre[0]['name'], 'Wrong genre name in response'

    async def test_one_genre_not_in_es(self, es_write_data, make_get_request):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        wrong_uuid = f'{genre_uuid}abc'
        await es_write_data(EsIndex.GENRE, genre)
        response = await make_get_request(f'{GENRES_URL}/{wrong_uuid}')

        assert response.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert response.body['detail'] == 'genre not found', 'Wrong error message'


class TestGenres:
    async def test_all_genre_default_page(self, es_write_data, make_get_request):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE + 1)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL)
        response_first_page = await make_get_request(GENRES_URL, {'page_number': 1})

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) == DEFAULT_PAGE_SIZE, 'Wrong page size in response'
        assert response == response_first_page, 'Default page and first page are not the same'
        for genre in response.body:
            assert 'uuid' in genre, 'No uuid in response'
            assert 'name' in genre, 'No genre name in response'

    @pytest.mark.parametrize('page_size', [1, 15, 19, 20, 21, '10', 200, 1000])
    async def test_all_genres_page_size(self, es_write_data, make_get_request, page_size):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_size': page_size})

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) <= int(page_size), 'Wrong page size in response'

    @pytest.mark.parametrize(
        'page_size, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer')
        ]
    )
    async def test_all_genres_invalid_pages(self, es_write_data, make_get_request, page_size, msg):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_size': page_size})

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_size', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'

    async def test_all_genres_compare_pages(self, es_write_data, make_get_request):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE * 2)
        await es_write_data(EsIndex.GENRE, genres)
        response_first_page = await make_get_request(GENRES_URL, {'page_number': 1})
        response_second_page = await make_get_request(GENRES_URL, {'page_number': 2})

        assert response_first_page.status == HTTPStatus.OK, 'Wrong status code'
        assert response_second_page.status == HTTPStatus.OK, 'Wrong status code'
        assert response_first_page != response_second_page, 'Pages are the same'

    @pytest.mark.parametrize('page_number', [15, '10', 200])
    async def test_all_genres_page_number(self, es_write_data, make_get_request, page_number):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.OK, 'Wrong status code'

    @pytest.mark.parametrize('page_number', [700, 1000])
    async def test_all_genres_page_number_max(self, es_write_data, make_get_request, page_number):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.BAD_REQUEST, 'Wrong status code'

    @pytest.mark.parametrize(
        'page_number, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer'),
        ]
    )
    async def test_all_genres_invalid_page_number(self, es_write_data, make_get_request, page_number, msg):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_number', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'

    @pytest.mark.parametrize('page_size, page_number', [(1, 15), (20, 200), ('10', '10')])
    async def test_all_genres(self, es_write_data, make_get_request, page_size, page_number):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE * 2)
        await es_write_data(EsIndex.GENRE, genres)
        response = await make_get_request(GENRES_URL, {'page_size': page_size, 'page_number': page_number})

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) <= int(page_size), 'Wrong page size in response'


class TestCache:
    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    async def test_one_genre_from_cache_redis(self, es_write_data, es_delete_data, make_get_request, diff_time):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        await es_write_data(EsIndex.GENRE, genre)
        await make_get_request(f'{GENRES_URL}/{genre_uuid}')
        await es_delete_data(EsIndex.GENRE, genre_uuid)
        await sleep(diff_time)
        response = await make_get_request(f'{GENRES_URL}/{genre_uuid}')

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert response.body['uuid'] == genre_uuid, 'Wrong uuid in response'

    async def test_one_genre_from_cache_redis_ttl_expired(self, es_write_data, es_delete_data, make_get_request):
        genre = await get_genres_data(1)
        genre_uuid = await get_genre_uuid(genre)
        await es_write_data(EsIndex.GENRE, genre)
        await make_get_request(f'{GENRES_URL}/{genre_uuid}')
        await es_delete_data(EsIndex.GENRE, genre_uuid)
        await sleep(CACHE_TTL + 1)
        response = await make_get_request(f'{GENRES_URL}/{genre_uuid}')

        assert response.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert response.body['detail'] == 'genre not found', 'Wrong error message'

    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    async def test_all_genres_from_cache_redis(self, es_write_data, es_delete_data, make_get_request, diff_time):
        genres = await get_genres_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.GENRE, genres)
        response_es = await make_get_request(GENRES_URL, {'page_size': 1, 'page_number': 1})
        for genre in genres:
            genre_uuid = await get_genre_uuid([genre])
            await es_delete_data(EsIndex.GENRE, genre_uuid)
        await sleep(diff_time)
        response_cache = await make_get_request(GENRES_URL, {'page_size': 1, 'page_number': 1})

        assert response_cache.status == HTTPStatus.OK, 'Wrong status code'
        assert response_es.body == response_cache.body, 'Response dont match'

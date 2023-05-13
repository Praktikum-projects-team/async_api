from asyncio import sleep

import pytest

from tests.functional.testdata.films import get_film_uuid_from_film_data, get_films_data, get_genre_uuid_from_film_data
from tests.functional.utils.checkers import check_ratings
from tests.functional.utils.constants import CACHE_TTL, DEFAULT_PAGE_SIZE, EsIndex, Sort
from tests.functional.utils.routes import FILMS_URL


class TestFilm:

    @pytest.mark.asyncio
    async def test_film_structure(self, es_write_data, make_get_request):
        film_data = await get_films_data(1)
        film_uuid = await get_film_uuid_from_film_data(film_data)
        await es_write_data(EsIndex.MOVIES, film_data)

        response = await make_get_request(f'{FILMS_URL}/{film_uuid}')

        assert response.status == 200, 'Wrong status code'
        assert 'uuid' in response.body, 'No uuid in response'
        assert 'title' in response.body, 'No title in response'
        assert 'imdb_rating' in response.body, 'No imdb_rating in response'
        assert 'description' in response.body, 'No description in response'
        assert 'directors' in response.body, 'No directors in response'
        assert 'actors' in response.body, 'No actors in response'
        assert 'writers' in response.body, 'No writers in response'
        assert 'genre' in response.body, 'No genre in response'
        assert response.body['uuid'] == film_uuid

    @pytest.mark.parametrize('film_uuid',
                             [0, '00af52ec-9345-4d66-adbe-50eb917f463a', 'wrong_uuid', '777']
                             )
    @pytest.mark.asyncio
    async def test_film_not_in_es(self, es_write_data, make_get_request, film_uuid):
        film_data = await get_films_data(1)
        await es_write_data(EsIndex.MOVIES, film_data)

        response = await make_get_request(f'{FILMS_URL}/{film_uuid}')

        assert response.status == 404, 'Wrong status code'
        assert response.body['detail'] == 'film not found', 'Wrong error message'


class TestFilms:
    @pytest.mark.asyncio
    async def test_films_structure(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL)

        assert response.status == 200, 'Wrong status code'
        for film in response.body:
            assert 'uuid' in film, 'No uuid in response'
            assert 'title' in film, 'No title in response'
            assert 'imdb_rating' in film, 'No imdb_rating in response'

    @pytest.mark.asyncio
    async def test_films_page_size_default(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL)

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == DEFAULT_PAGE_SIZE, 'Wrong page size in response'

    @pytest.mark.parametrize('page_size', [1, 15, 19, 20, 21, '10'])
    @pytest.mark.asyncio
    async def test_films_page_size(self, es_write_data, make_get_request, page_size):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_size': page_size})

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == int(page_size), 'Wrong page size in response'

    @pytest.mark.asyncio
    async def test_films_page_size_max(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_size': DEFAULT_PAGE_SIZE + 1000})

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) <= DEFAULT_PAGE_SIZE + 1000, 'Wrong page size in response'

    @pytest.mark.parametrize(
        'page_size, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer'),
        ]
    )
    @pytest.mark.asyncio
    async def test_films_page_size_incorrect(self, es_write_data, make_get_request, page_size, msg):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_size': page_size})

        assert response.status == 422, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_size', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'

    @pytest.mark.asyncio
    async def test_films_page_number_default(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response_without_page_number = await make_get_request(FILMS_URL)
        response_with_page_number_1 = await make_get_request(FILMS_URL, {'page_number': 1})

        assert response_with_page_number_1.status == 200, 'Wrong status code'
        assert response_without_page_number == response_with_page_number_1, 'Pages are not the same'

    @pytest.mark.asyncio
    async def test_films_page_number_compare(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE*2)
        await es_write_data(EsIndex.MOVIES, films_data)

        response_with_page_number_1 = await make_get_request(FILMS_URL, {'page_number': 1})
        response_with_page_number_2 = await make_get_request(FILMS_URL, {'page_number': 2})

        assert response_with_page_number_1.status == 200, 'Wrong status code'
        assert response_with_page_number_1 != response_with_page_number_2, 'Pages are the same'

    @pytest.mark.parametrize('page_number', [15, 200, '10'])
    @pytest.mark.asyncio
    async def test_films_page_number(self, es_write_data, make_get_request, page_number):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_number': page_number})

        assert response.status == 200, 'Wrong status code'

    @pytest.mark.parametrize('page_number', [700, 1000, 2000])
    @pytest.mark.asyncio
    async def test_films_page_number_max(self, es_write_data, make_get_request, page_number):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_number': page_number})

        assert response.status == 400, 'Wrong status code'

    @pytest.mark.parametrize(
        'page_number, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer'),
        ]
    )
    @pytest.mark.asyncio
    async def test_films_page_number_incorrect(self, es_write_data, make_get_request, page_number, msg):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'page_number': page_number})

        assert response.status == 422, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_number', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'

    @pytest.mark.asyncio
    async def test_films_sort_default(self, es_write_data, make_get_request):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response_without_sort = await make_get_request(FILMS_URL)
        response_with_sort = await make_get_request(FILMS_URL, {'sort': Sort.DESC})

        assert response_with_sort.status == 200, 'Wrong status code'
        assert response_without_sort == response_with_sort, 'Sorts are not the same'

    @pytest.mark.parametrize('sort', [Sort.DESC, Sort.ASC])
    @pytest.mark.asyncio
    async def test_films_sort(self, es_write_data, make_get_request, sort):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'sort': sort})
        imdb_ratings = [film['imdb_rating'] for film in response.body]

        assert response.status == 200, 'Wrong status code'
        await check_ratings(imdb_ratings, sort)

    @pytest.mark.parametrize('sort', [
        0, 1, -1, 2.5, 'sort', '%#$*',
    ])
    @pytest.mark.asyncio
    async def test_films_sort_incorrect(self, es_write_data, make_get_request, sort):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'sort': sort})

        assert response.status == 400, 'Wrong status code'

    @pytest.mark.parametrize(
        'number_of_films_by_genre', [1, 10, 20]
    )
    @pytest.mark.asyncio
    async def test_films_filter_genre(self, es_write_data, make_get_request, number_of_films_by_genre):
        """Checking that all movies by genre are found"""
        films_data = await get_films_data(number_of_films_by_genre)
        genre_uuid = await get_genre_uuid_from_film_data(films_data)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'genre': genre_uuid})

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == number_of_films_by_genre, 'Wrong number of films by genre'

    @pytest.mark.parametrize('genre_uuid', [
        '77777777-0d90-4353-88ba-4ccc5d2c07ff', 'Western', 0, 1, -1, 2.5, '%#$*',
    ])
    @pytest.mark.asyncio
    async def test_films_filter_genre_incorrect(self, es_write_data, make_get_request, genre_uuid):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, {'genre': genre_uuid})

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == 0, 'Wrong number of films by genre'

    @pytest.mark.parametrize('query_params', [
        {'sort': Sort.DESC, 'page_size': 1, 'page_number': 1},
        {'sort': Sort.DESC, 'page_size': 100, 'page_number': 50},
        {'sort': Sort.ASC, 'page_size': 5, 'page_number': 5},
        {'sort': Sort.ASC, 'page_size': 200, 'page_number': 3}
    ])
    @pytest.mark.asyncio
    async def test_films_params(self, es_write_data, make_get_request, query_params):
        films_data = await get_films_data(DEFAULT_PAGE_SIZE)
        genre_uuid = await get_genre_uuid_from_film_data(films_data)
        query_params.update({'genre': genre_uuid})
        await es_write_data(EsIndex.MOVIES, films_data)

        response = await make_get_request(FILMS_URL, query_params)

        assert response.status == 200, 'Wrong status code'


class TestCache:

    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    @pytest.mark.asyncio
    async def test_film_from_cache_redis(self, es_write_data, es_delete_data, make_get_request, diff_time):
        film_data = await get_films_data(1)
        film_uuid = await get_film_uuid_from_film_data(film_data)
        await es_write_data(EsIndex.MOVIES, film_data)
        await make_get_request(f'{FILMS_URL}/{film_uuid}')
        await es_delete_data(EsIndex.MOVIES, film_uuid)
        await sleep(diff_time)

        response = await make_get_request(f'{FILMS_URL}/{film_uuid}')

        assert response.status == 200, 'Wrong status code'
        assert response.body.get('uuid') == film_uuid, 'Wrong uuid in response'

    @pytest.mark.asyncio
    async def test_film_from_cache_redis_ttl_expired(self, es_write_data, es_delete_data, make_get_request):
        film_data = await get_films_data(1)
        film_uuid = await get_film_uuid_from_film_data(film_data)
        await es_write_data(EsIndex.MOVIES, film_data)
        await make_get_request(f'{FILMS_URL}/{film_uuid}')
        await es_delete_data(EsIndex.MOVIES, film_uuid)
        await sleep(CACHE_TTL + 1)

        response = await make_get_request(f'{FILMS_URL}/{film_uuid}')

        assert response.status == 404, 'Wrong status code'
        assert response.body['detail'] == 'film not found', 'Wrong error message'

    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    @pytest.mark.asyncio
    async def test_films_params_form_cache_redid(
            self, es_write_data, es_delete_data, make_get_request, diff_time
    ):
        films_data = await get_films_data(3)
        genre_uuid = await get_genre_uuid_from_film_data(films_data)
        query_params = {'sort': Sort.DESC, 'page_size': 1, 'page_number': 1, 'genre': genre_uuid}
        await es_write_data(EsIndex.MOVIES, films_data)
        response_es = await make_get_request(FILMS_URL, query_params)

        for film_data in films_data:
            film_uuid = await get_film_uuid_from_film_data([film_data])
            await es_delete_data(EsIndex.MOVIES, film_uuid)
        await sleep(diff_time)
        response_cache = await make_get_request(FILMS_URL, query_params)

        assert response_cache.status == 200, 'Wrong status code'
        assert response_es.body == response_cache.body, 'Response dont match'

    @pytest.mark.asyncio
    async def test_films_params_form_cache_redid_ttl_expired(
            self, es_write_data, es_delete_data, make_get_request
    ):
        films_data = await get_films_data(3)
        genre_uuid = await get_genre_uuid_from_film_data(films_data)
        query_params = {'sort': Sort.DESC, 'page_size': 1, 'page_number': 1, 'genre': genre_uuid}
        await es_write_data(EsIndex.MOVIES, films_data)
        await make_get_request(FILMS_URL, query_params)

        for film_data in films_data:
            film_uuid = await get_film_uuid_from_film_data([film_data])
            await es_delete_data(EsIndex.MOVIES, film_uuid)
        await sleep(CACHE_TTL + 1)

        response = await make_get_request(FILMS_URL, query_params)

        assert response.status == 200, 'Wrong status code'
        assert len(response.body) == 0, 'Wrong error message'

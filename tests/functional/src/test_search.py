import pytest
from asyncio import sleep
from http import HTTPStatus

from tests.functional.testdata.films import get_films_data, get_film_uuid_from_film_data
from tests.functional.testdata.genres import get_genres_data, get_genre_uuid
from tests.functional.testdata.persons import get_persons_data, get_person_uuid_from_person_data
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE, EsIndex
from tests.functional.utils.routes import FILMS_SEARCH_URL, GENRES_SEARCH_URL, PERSONS_SEARCH_URL
from tests.functional.testdata.genres_query import genres_search_query
from tests.functional.testdata.films_query import films_search_query
from tests.functional.testdata.persons_query import persons_search_query

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize(
    'query_data, diff_time, expected_answer', [
        *films_search_query
    ]
)
async def test_films_search(es_write_data, make_get_request, es_delete_data, query_data, diff_time, expected_answer):
    films_data = await get_films_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.MOVIES, films_data)
    response_es = await make_get_request(FILMS_SEARCH_URL, query_data)

    for film in films_data:
        film_uuid = await get_film_uuid_from_film_data([film])
        await es_delete_data(EsIndex.MOVIES, film_uuid)
    await sleep(diff_time)
    response_cache = await make_get_request(FILMS_SEARCH_URL, query_data)
    assert response_es.status == expected_answer['status']
    assert len(response_es.body) == expected_answer['len']
    assert response_cache.status == expected_answer['cache_status']
    if expected_answer['cache_status'] == HTTPStatus.OK:
        assert response_es.body == response_cache.body


@pytest.mark.parametrize(
    'query_data, diff_time, expected_answer', [
        *genres_search_query
    ]
)
async def test_genres_search(es_write_data, make_get_request, es_delete_data, query_data, diff_time, expected_answer):
    genres = await get_genres_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.GENRE, genres)
    response_es = await make_get_request(GENRES_SEARCH_URL, query_data)
    for genre in genres:
        genre_uuid = await get_genre_uuid([genre])
        await es_delete_data(EsIndex.GENRE, genre_uuid)
    await sleep(diff_time)
    response_cache = await make_get_request(GENRES_SEARCH_URL, query_data)
    assert response_es.status == expected_answer['status']
    assert len(response_es.body) == expected_answer['len']
    assert response_cache.status == expected_answer['cache_status']
    if expected_answer['cache_status'] == HTTPStatus.OK:
        assert response_es.body == response_cache.body


@pytest.mark.parametrize(
    'query_data, diff_time, expected_answer', [
        *persons_search_query
    ]
)
async def test_persons_search(es_write_data, make_get_request, es_delete_data, query_data, diff_time, expected_answer):
    persons = await get_persons_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.PERSON, persons)
    response_es = await make_get_request(PERSONS_SEARCH_URL, query_data)
    for person in persons:
        person_uuid = await get_person_uuid_from_person_data([person])
        await es_delete_data(EsIndex.PERSON, person_uuid)
    await sleep(diff_time)
    response_cache = await make_get_request(PERSONS_SEARCH_URL, query_data)
    assert response_es.status == expected_answer['status']
    assert len(response_es.body) == expected_answer['len']
    assert response_cache.status == expected_answer['cache_status']
    if expected_answer['cache_status'] == HTTPStatus.OK:
        assert response_es.body == response_cache.body

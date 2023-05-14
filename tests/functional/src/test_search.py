import pytest
from asyncio import sleep
from http import HTTPStatus

from tests.functional.testdata.films import get_films_data
from tests.functional.testdata.genres import get_genres_data, get_genre_uuid
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE, EsIndex, CACHE_TTL
from tests.functional.utils.routes import FILMS_SEARCH_URL, GENRES_SEARCH_URL
from tests.functional.testdata.genres_query import genres_search_query


@pytest.mark.parametrize(
    'query_data, expected_answer', [
        ({'query': 'The Star'}, {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE}),
        ({'query': 'Mashed potato'}, {'status': HTTPStatus.OK, 'len': 0})
    ]
)
@pytest.mark.asyncio
async def test_films_search(es_write_data, make_get_request, query_data, expected_answer):
    films_data = await get_films_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.MOVIES, films_data)

    response = await make_get_request(FILMS_SEARCH_URL, query_data)

    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['len']


@pytest.mark.parametrize(
    'query_data, diff_time, expected_answer', [
        *genres_search_query
    ]
)
@pytest.mark.asyncio
async def test_genres_search(es_write_data, make_get_request, es_delete_data, query_data, diff_time, expected_answer):
    genres = await get_genres_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.GENRE, genres)
    response_es = await make_get_request(GENRES_SEARCH_URL, query_data)
    for genre in genres:
        genre_uuid = await get_genre_uuid([genre])
        await es_delete_data(EsIndex.GENRE, {'query': {'match': {'uuid': genre_uuid}}})
    await sleep(diff_time)
    response_cache = await make_get_request(GENRES_SEARCH_URL, query_data)
    assert response_es.status == expected_answer['status']
    assert len(response_es.body) == expected_answer['len']
    assert response_cache.status == expected_answer['cache_status']
    if expected_answer['cache_status'] == HTTPStatus.OK:
        assert response_es.body == response_cache.body

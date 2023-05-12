import pytest

from tests.functional.testdata.films import get_films_data
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE, EsIndex
from tests.functional.utils.routes import FILMS_SEARCH_URL


@pytest.mark.parametrize(
    'query_data, expected_answer', [
        ({'query': 'The Star'}, {'status': 200, 'len': DEFAULT_PAGE_SIZE}),
        ({'query': 'Mashed potato'}, {'status': 200, 'len': 0})
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request, query_data, expected_answer):
    films_data = await get_films_data(DEFAULT_PAGE_SIZE)
    await es_write_data(EsIndex.MOVIES, films_data)

    response = await make_get_request(FILMS_SEARCH_URL, query_data)

    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['len']

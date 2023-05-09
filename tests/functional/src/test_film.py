import pytest
# from tests.functional.conftest import es_write_data, make_get_request
from tests.functional.settings import test_settings
from tests.functional.testdata.search_film_collections import search_50_data


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star'},
                {'status': 200, 'len': 50}
        ),
        (
                {'query': 'Mashed potato'},
                {'status': 200, 'len': 0}
        )
    ]
)
@pytest.mark.asyncio
async def test_search(es_write_data,
                      make_get_request,
                      query_data,
                      expected_answer):
    await es_write_data(test_settings.es_index, search_50_data)
    url = test_settings.service_url + '/api/v1/films/search'

    response = await make_get_request(url, query_data)

    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['len']

# import pytest
#
#
# @pytest.mark.asyncio
# async def test_debug():
#     pass
#
#
# @pytest.mark.parametrize(
#     'query_data, expected_answer',
#     [
#         (
#                 {'search': 'The Star'},
#                 {'status': 200, 'length': 50}
#         ),
#         (
#                 {'search': 'Mashed potato'},
#                 {'status': 200, 'length': 0}
#         )
#     ]
# )
# @pytest.mark.asyncio
# async def test_search(es_write_data, query_data, expected_answer):
#     es_data = [{
#         # ....
#     } for _ in range(60)]
#
#     await es_write_data(es_data)


import datetime
import json
import uuid
import orjson

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.conftest import es_write_data, make_get_request
from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import common_index_settings, index_mappings
from tests.functional.testdata.search_film_collections import search_50_data


@pytest.mark.parametrize(
    'es_data',
    [search_50_data]
)
@pytest.mark.asyncio
async def test_search(es_write_data, make_get_request, es_data):
    await es_write_data(test_settings.es_index, es_data)

    url = test_settings.service_url + '/api/v1/films/search'
    query_data = {'query': 'The Star'}

    response = await make_get_request(url, query_data)

    assert response.status == 200
    assert len(response.body) == 50



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

from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import common_index_settings, index_mappings


@pytest.mark.asyncio
async def test_search():
    # 1. Генерируем данные для ES


    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genre': [],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': str(uuid.uuid4()), 'name': 'Ann'},
            {'id': str(uuid.uuid4()), 'name': 'Bob'}
        ],
        'writers': [
            {'id': str(uuid.uuid4()), 'name': 'Ben'},
            {'id': str(uuid.uuid4()), 'name': 'Howard'}
        ]
    } for _ in range(50)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.es_index, '_id': row[test_settings.es_id_field]}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    # 2. Загружаем данные в ES

    # es_client = AsyncElasticsearch(hosts=test_settings.es_host,
    #                                validate_cert=False,
    #                                use_ssl=False)
    # await es_client.indices.create(index=test_settings.es_index, body={'mappings': index_mappings[test_settings.es_index], 'settings': common_index_settings})
    # response = await es_client.bulk(str_query, refresh=True)
    # await es_client.close()


    # if response['errors']:
    #     raise Exception(f"{response['errors']}")

    # # 3. Запрашиваем данные из ES по API
    #
    session = aiohttp.ClientSession()
    url = test_settings.service_url + '/api/v1/films/search'
    query_data = {'query': 'The Star'}
    async with session.get('http://fastapi:8000/api/v1/films/search', params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ

    assert status == 200
    assert len(body) == 50



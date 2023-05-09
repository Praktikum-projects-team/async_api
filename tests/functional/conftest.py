import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import index_mappings, common_index_settings


def get_es_bulk_query(index_name: str, data: list[dict]) -> str:
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': index_name, '_id': row[test_settings.es_id_field]}}),
            json.dumps(row)
        ])
    q_str = '\n'.join(bulk_query) + '\n'
    return q_str


async def create_index_if_not_exists(es_client, index_name):
    if await es_client.indices.exists(index=index_name):
        return
    await es_client.indices.create(
        index=test_settings.es_index,
        body={'mappings': index_mappings[index_name], 'settings': common_index_settings}
    )


@pytest.fixture
def es_write_data():
    async def inner(index: str, data: list[dict]):
        str_query = get_es_bulk_query(index, data)
        # print(f'{str_query}!!!!!!!!!!!!!!!!!!')

        es_client = AsyncElasticsearch(hosts=test_settings.es_host,
                                       validate_cert=False,
                                       use_ssl=False)
        await create_index_if_not_exists(es_client, index_name=index)
        response = await es_client.bulk(str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner

# es_data = [{
#     'id': str(uuid.uuid4()),
#     'imdb_rating': 8.5,
#     'genre': [],
#     'title': 'The Star',
#     'description': 'New World',
#     'director': ['Stan'],
#     'actors_names': ['Ann', 'Bob'],
#     'writers_names': ['Ben', 'Howard'],
#     'actors': [
#         {'id': str(uuid.uuid4()), 'name': 'Ann'},
#         {'id': str(uuid.uuid4()), 'name': 'Bob'}
#     ],
#     'writers': [
#         {'id': str(uuid.uuid4()), 'name': 'Ben'},
#         {'id': str(uuid.uuid4()), 'name': 'Howard'}
#     ]
# } for _ in range(50)]
#
# print(get_es_bulk_query('movies', es_data))

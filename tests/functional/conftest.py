import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import get_es_bulk_query, create_index_if_not_exists, ApiResponse


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host, validate_cert=False, use_ssl=False)
    yield client
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(index: str, data: list[dict]):
        str_query = get_es_bulk_query(index, data)

        await create_index_if_not_exists(es_client, index_name=index)
        response = await es_client.bulk(str_query, refresh=True)
        await es_client.close()
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def make_get_request():
    async def inner(url: str, query_data: list[dict]):
        session = aiohttp.ClientSession()
        async with session.get(url, params=query_data) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        await session.close()
        return resp
    return inner


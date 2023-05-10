import aiohttp
import pytest
import asyncio

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import get_es_bulk_query, create_index_if_not_exists, ApiResponse


# Регистрация чекеров в pytest
pytest.register_assert_rewrite('tests.functional.utils.checkers')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host, validate_cert=False, use_ssl=False)
    yield client
    # Удаляем все тестовые данные после сессии
    await client.indices.delete(index='*', ignore=[400, 404])
    await client.close()


@pytest.fixture(scope='session')
async def aiohttp_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
async def es_write_data(es_client):
    async def inner(index: str, data: list[dict]):
        await create_index_if_not_exists(es_client, index_name=index)

        str_query = get_es_bulk_query(index, data)
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

    return inner


@pytest.fixture
async def es_delete_data(es_client):
    async def inner(index: str, query: dict):
        if await es_client.indices.exists(index=index):
            await es_client.delete_by_query(index=index, body=query)
        else:
            raise Exception('Индекс не найден в Elasticsearch')

    return inner


@pytest.fixture
async def make_get_request(aiohttp_session):
    async def inner(path: str, query_data: dict = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        async with aiohttp_session.get(url, params=query_data) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp
    return inner

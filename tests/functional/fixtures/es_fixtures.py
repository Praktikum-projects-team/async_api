import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings
from tests.functional.utils.helpers import get_es_bulk_query, create_index_if_not_exists


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host, validate_cert=False, use_ssl=False)
    yield client
    # Удаляем все тестовые данные после сессии
    await client.indices.delete(index='*', ignore=[400, 404])
    await client.close()


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
    async def inner(index: str, query):
        if await es_client.indices.exists(index=index):
            await es_client.delete(index=index, id=query)
        else:
            raise Exception('Индекс не найден в Elasticsearch')

    return inner

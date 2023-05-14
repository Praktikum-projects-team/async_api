import pytest
from tests.functional.settings import test_settings
from tests.functional.utils.helpers import ApiResponse


@pytest.fixture
async def make_get_request(aiohttp_session):
    async def inner(path: str, query_data: dict = None):
        url = f'http://{test_settings.api_host}:{test_settings.api_port}' + path
        async with aiohttp_session.get(url, params=query_data) as response:
            resp = ApiResponse(status=response.status, body=await response.json())
        return resp

    return inner

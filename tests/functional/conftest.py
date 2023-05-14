import pytest
import asyncio

# Регистрация чекеров в pytest
pytest.register_assert_rewrite('tests.functional.utils.checkers')

pytest_plugins = ('tests.functional.fixtures.es_fixtures', 'tests.functional.fixtures.request_fixtures')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

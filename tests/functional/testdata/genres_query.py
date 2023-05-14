from http import HTTPStatus
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE, CACHE_TTL

# params format: 'query_data, diff_time, expected_answer'

genres_search_query = [
        ({'query': 'Action'}, 0, {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE, 'cache_status': HTTPStatus.OK}),
        ({'query': 'action'}, CACHE_TTL - 1,
         {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE, 'cache_status': HTTPStatus.OK}),
        ({'query': 'Action', 'page_size': 1}, CACHE_TTL,
         {'status': HTTPStatus.OK, 'len': 1, 'cache_status': HTTPStatus.OK}),
        ({'query': 'Action', 'page_size': 100}, CACHE_TTL + 1,
         {'status': HTTPStatus.OK, 'len': 100, 'cache_status': HTTPStatus.OK}),
        ({'query': 'Action', 'page_size': -1}, 0, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'len': 1, 'cache_status': HTTPStatus.UNPROCESSABLE_ENTITY}),
        ({'query': 'Action', 'page_number': 1}, CACHE_TTL - 1,
         {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE, 'cache_status': HTTPStatus.OK}),
        ({'query': 'Action', 'page_number': -1}, CACHE_TTL + 1, {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'len': 1, 'cache_status': HTTPStatus.UNPROCESSABLE_ENTITY}),
        ({'query': 'Action', 'page_size': 1, 'page_number': 1}, 0,
         {'status': HTTPStatus.OK, 'len': 1, 'cache_status': HTTPStatus.OK}),
        ({'query': 'Genres'}, CACHE_TTL, {'status': HTTPStatus.NOT_FOUND, 'len': 1, 'cache_status': HTTPStatus.NOT_FOUND})
    ]
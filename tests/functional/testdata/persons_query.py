from http import HTTPStatus
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE, CACHE_TTL

# params format: 'query_data, diff_time, expected_answer'

persons_search_query = [
    ({'query': 'George Lucas'}, 0, {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE, 'cache_status': HTTPStatus.OK}),
    ({'query': 'george,'}, 0, {'status': HTTPStatus.OK, 'len': DEFAULT_PAGE_SIZE, 'cache_status': HTTPStatus.OK}),
    ({'query': 'Mr. Somebody'}, CACHE_TTL - 1,
     {'status': HTTPStatus.NOT_FOUND, 'len': 1, 'cache_status': HTTPStatus.NOT_FOUND}),
    ({'query': 'lucas', 'page_size': 1}, CACHE_TTL, {'status': HTTPStatus.OK, 'len': 1, 'cache_status': HTTPStatus.OK}),
    ({'query': 'george Lucas', 'page_size': 100}, CACHE_TTL + 1,
     {'status': HTTPStatus.OK, 'len': 100, 'cache_status': HTTPStatus.OK}),
    ({'query': 'George', 'page_size': -15}, 0,
     {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'len': 1, 'cache_status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'query': 'George', 'page_number': -7}, CACHE_TTL + 1,
     {'status': HTTPStatus.UNPROCESSABLE_ENTITY, 'len': 1, 'cache_status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ({'query': 'Lucas', 'page_size': 1, 'page_number': 1}, 0,
     {'status': HTTPStatus.OK, 'len': 1, 'cache_status': HTTPStatus.OK}),

]

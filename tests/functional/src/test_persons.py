import pytest
from asyncio import sleep
from http import HTTPStatus

from tests.functional.testdata.persons import get_person_uuid_from_person_data, get_persons_data
from tests.functional.utils.constants import CACHE_TTL, DEFAULT_PAGE_SIZE, EsIndex

from tests.functional.utils.routes import PERSONS_URL


class TestPerson:

    @pytest.mark.asyncio
    async def test_person_structure(self, es_write_data, make_get_request):
        person_data = await get_persons_data(1)
        person_uuid = await get_person_uuid_from_person_data(person_data)

        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(f'{PERSONS_URL}/{person_uuid}')

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert 'uuid' in response.body, 'No person_uuid in response'
        assert 'full_name' in response.body, 'No title in response'
        assert 'films' in response.body, 'No imdb_rating in response'
        assert 'role' in response.body['films'][0], 'No role in response'
        assert 'uuid' in response.body['films'][0], 'No person_uuid in response'
        assert response.body['uuid'] == person_uuid

    @pytest.mark.parametrize('person_uuid',
                             [0, '00af52ec-9345-4d66-adbe-50eb917f463a', 'wrong_uuid', '777']
                             )
    @pytest.mark.asyncio
    async def test_person_not_in_es(self, es_write_data, make_get_request, person_uuid):
        person_data = await get_persons_data(1)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(f'{PERSONS_URL}/{person_uuid}')

        assert response.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert response.body['detail'] == 'person not found', 'Wrong error message'


class TestPersons:

    @pytest.mark.asyncio
    async def test_persons_structure(self, es_write_data, make_get_request):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(PERSONS_URL)

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert 'uuid' in response.body[0], 'No person_uuid in response'
        assert 'full_name' in response.body[0], 'No title in response'
        assert 'films' in response.body[0], 'No imdb_rating in response'
        assert 'role' in response.body[0]['films'][0], 'No role in response'
        assert 'uuid' in response.body[0]['films'][0], 'No person_uuid in response'

    @pytest.mark.asyncio
    async def test_persons_page_size_default(self, es_write_data, make_get_request):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(PERSONS_URL)

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) == DEFAULT_PAGE_SIZE, 'Wrong page size in response'

    @pytest.mark.parametrize('page_size', [1, 15, 19, 20, 21, '10'])
    @pytest.mark.asyncio
    async def test_persons_page_size(self, es_write_data, make_get_request, page_size):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(PERSONS_URL, {'page_size': page_size})

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) == int(page_size), 'Wrong page size in response'

    @pytest.mark.asyncio
    async def test_persons_page_size_max(self, es_write_data, make_get_request):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(PERSONS_URL, {'page_size': DEFAULT_PAGE_SIZE + 1000})

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert len(response.body) <= DEFAULT_PAGE_SIZE + 1000, 'Wrong page size in response'

    @pytest.mark.parametrize(
        'page_size, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer'),
        ]
    )
    @pytest.mark.asyncio
    async def test_persons_page_size_incorrect(self, es_write_data, make_get_request, page_size, msg):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response = await make_get_request(PERSONS_URL, {'page_size': page_size})

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_size', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'

    @pytest.mark.asyncio
    async def test_persons_page_number_default(self, es_write_data, make_get_request):
        person_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, person_data)

        response_without_page_number = await make_get_request(PERSONS_URL)
        response_with_page_number_1 = await make_get_request(PERSONS_URL, {'page_number': 1})

        assert response_with_page_number_1.status == HTTPStatus.OK, 'Wrong status code'
        assert response_without_page_number == response_with_page_number_1, 'Pages are not the same'

    @pytest.mark.asyncio
    async def test_persons_page_number_compare(self, es_write_data, make_get_request):
        persons_data = await get_persons_data(DEFAULT_PAGE_SIZE*2)
        await es_write_data(EsIndex.PERSON, persons_data)

        response_with_page_number_1 = await make_get_request(PERSONS_URL, {'page_number': 1})
        response_with_page_number_2 = await make_get_request(PERSONS_URL, {'page_number': 2})

        assert response_with_page_number_1.status == HTTPStatus.OK, 'Wrong status code'
        assert response_with_page_number_1 != response_with_page_number_2, 'Pages are the same'

    @pytest.mark.parametrize('page_number', [4, 15, '10', 100, 200])
    @pytest.mark.asyncio
    async def test_persons_page_number(self, es_write_data, make_get_request, page_number):
        persons_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, persons_data)

        response = await make_get_request(PERSONS_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.OK, 'Wrong status code'

    @pytest.mark.parametrize('page_number', [300, 400])
    @pytest.mark.asyncio
    async def test_persons_page_number_more(self, es_write_data, make_get_request, page_number):
        persons_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, persons_data)

        response = await make_get_request(PERSONS_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert response.body['detail'] == 'persons not found', 'Wrong error message'

    @pytest.mark.parametrize('page_number', [700, 1000, 2000])
    @pytest.mark.asyncio
    async def test_persons_page_number_max(self, es_write_data, make_get_request, page_number):
        persons_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, persons_data)

        response = await make_get_request(PERSONS_URL, {'page_number': page_number})

        assert response.status == 400, 'Wrong status code'

    @pytest.mark.parametrize(
        'page_number, msg', [
            (0, 'ensure this value is greater than or equal to 1'),
            (-1, 'ensure this value is greater than or equal to 1'),
            (2.5, 'value is not a valid integer'),
            ('pagesize', 'value is not a valid integer'),
            ('%#$*', 'value is not a valid integer'),
        ]
    )
    @pytest.mark.asyncio
    async def test_persons_page_number_incorrect(self, es_write_data, make_get_request, page_number, msg):
        persons_data = await get_persons_data(DEFAULT_PAGE_SIZE)
        await es_write_data(EsIndex.PERSON, persons_data)

        response = await make_get_request(PERSONS_URL, {'page_number': page_number})

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Wrong status code'
        assert response.body['detail'][0]['loc'][1] == 'page_number', 'Wrong error location'
        assert response.body['detail'][0]['msg'] == msg, 'Wrong error message'


@pytest.mark.debug
class TestCache:

    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    @pytest.mark.asyncio
    async def test_film_from_cache_redis(self, es_write_data, es_delete_data, make_get_request, diff_time):
        person_data = await get_persons_data(1)
        person_uuid = await get_person_uuid_from_person_data(person_data)
        await es_write_data(EsIndex.PERSON, person_data)
        await make_get_request(f'{PERSONS_URL}/{person_uuid}')
        await es_delete_data(EsIndex.PERSON, person_uuid)
        await sleep(diff_time)

        response = await make_get_request(f'{PERSONS_URL}/{person_uuid}')

        assert response.status == HTTPStatus.OK, 'Wrong status code'
        assert response.body.get('uuid') == person_uuid, 'Wrong uuid in response'

    @pytest.mark.asyncio
    async def test_film_from_cache_redis_ttl_expired(self, es_write_data, es_delete_data, make_get_request):
        person_data = await get_persons_data(1)
        person_uuid = await get_person_uuid_from_person_data(person_data)
        await es_write_data(EsIndex.PERSON, person_data)
        await make_get_request(f'{PERSONS_URL}/{person_uuid}')
        await es_delete_data(EsIndex.PERSON, person_uuid)
        await sleep(CACHE_TTL + 1)

        response = await make_get_request(f'{PERSONS_URL}/{person_uuid}')

        assert response.status == HTTPStatus.NOT_FOUND, 'Wrong status code'
        assert response.body['detail'] == 'person not found', 'Wrong error message'

    @pytest.mark.parametrize('diff_time', [0, CACHE_TTL - 1])
    @pytest.mark.asyncio
    async def test_films_params_form_cache_redid(
            self, es_write_data, es_delete_data, make_get_request, diff_time
    ):
        films_data = await get_persons_data(3)
        query_params = {'page_size': 1, 'page_number': 1}
        await es_write_data(EsIndex.PERSON, films_data)
        response_es = await make_get_request(PERSONS_URL, query_params)

        for person_data in films_data:
            person_uuid = await get_person_uuid_from_person_data([person_data])
            await es_delete_data(EsIndex.PERSON, person_uuid)
        await sleep(diff_time)
        response_cache = await make_get_request(PERSONS_URL, query_params)

        assert response_cache.status == HTTPStatus.OK, 'Wrong status code'
        assert response_es.body == response_cache.body, 'Response dont match'

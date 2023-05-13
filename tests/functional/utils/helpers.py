import json
from http import HTTPStatus
from typing import Union

from pydantic import BaseModel

from tests.functional.settings import test_settings
from tests.functional.testdata.es_mapping import index_mappings, common_index_settings


class ApiResponse(BaseModel):
    status: HTTPStatus
    body: Union[list, dict]


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
        index=index_name,
        body={'mappings': index_mappings[index_name], 'settings': common_index_settings}
    )

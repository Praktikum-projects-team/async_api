import backoff
from elasticsearch import Elasticsearch, ConnectionError

from tests.functional.settings import test_settings


@backoff.on_exception(
    backoff.expo,
    ConnectionError,
    max_tries=10,
)
def wait_es(es_client):
    es_client.ping()


if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{test_settings.es_host}:{test_settings.es_port}', validate_cert=False, use_ssl=False
    )
    wait_es(es_client)

import logging
import time

from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{test_settings.es_host}:{test_settings.es_port}', validate_cert=False, use_ssl=False
    )
    while True:
        try:
            es_client.ping()
            logging.info('Elasticsearch started')
            break
        except ConnectionError:
            time.sleep(1)
            logging.info('Waiting for elasticsearch to start...')

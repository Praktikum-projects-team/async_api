import logging
import time

from elasticsearch import Elasticsearch

from tests.functional import settings


elastic_config = settings.ElasticConfig()


if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=f'http://{elastic_config.host}:{elastic_config.port}', validate_cert=False, use_ssl=False
    )
    while True:
        try:
            es_client.ping()
            logging.info('Elasticsearch started')
            break
        except ConnectionError:
            time.sleep(1)
            logging.info('Waiting for elasticsearch to start...')

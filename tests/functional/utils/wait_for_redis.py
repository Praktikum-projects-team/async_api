import logging
import time

import redis

from tests.functional.settings import test_settings

if __name__ == '__main__':
    redis_client = redis.Redis(host=test_settings.redis_host, port=test_settings.redis_port, db=0)
    while True:
        try:
            redis_client.ping()
            logging.info('Redis started')
            break
        except redis.ConnectionError:
            time.sleep(1)
            logging.info('Waiting for Redis to start...')

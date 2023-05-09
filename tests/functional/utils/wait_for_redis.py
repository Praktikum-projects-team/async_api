import logging
import time

import redis

from tests.functional import settings

redis_config = settings.RedisConfig()


if __name__ == '__main__':
    redis_client = redis.Redis(host=redis_config.host, port=redis_config.port, db=0)
    while True:
        try:
            redis_client.ping()
            logging.info('Redis started')
            break
        except redis.ConnectionError:
            time.sleep(1)
            logging.info('Waiting for Redis to start...')

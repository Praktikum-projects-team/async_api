import backoff
import redis

from tests.functional.settings import test_settings


@backoff.on_exception(
    backoff.expo,
    redis.ConnectionError,
    max_tries=10,
)
def wait_redis(redis_client):
    redis_client.ping()


if __name__ == '__main__':
    redis_client = redis.Redis(host=test_settings.redis_host, port=test_settings.redis_port, db=0)
    wait_redis(redis_client)

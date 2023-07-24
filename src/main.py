import logging
from http import HTTPStatus

import logstash
import sentry_sdk
import uvicorn
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch, RequestError
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis

load_dotenv()

app_config = config.AppConfig()
elastic_config = config.ElasticConfig()
redis_config = config.RedisConfig()
logstash_config = config.LogstashConfig()
sentry_config = config.SentryConfig()

sentry_sdk.init(
    dsn=sentry_config.dsn,
    traces_sample_rate=0.4,
)

app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    logstash.LogstashHandler(
        host=logstash_config.logstash_host,
        port=logstash_config.logstash_port,
        version=1,
    )
)


@app.on_event('startup')
async def startup():
    redis.redis = Redis(host=redis_config.host, port=redis_config.port)
    elastic.es = AsyncElasticsearch(hosts=[f'{elastic_config.host}:{elastic_config.port}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


@app.middleware("http")
async def request_id_to_logger(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    request.app.state.logger = logging.LoggerAdapter(
        logger=logger,
        extra={'tags': ['async_api'], 'X-Request-Id': request_id},
    )
    return await call_next(request)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])


@app.exception_handler(RequestError)
async def bad_storage_request_exception_handler(request, exc):
    http_exc = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.error)
    return await http_exception_handler(request, http_exc)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )

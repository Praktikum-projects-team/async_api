import os
from logging import config as logging_config
from pydantic import BaseSettings, Field
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    base_dir: str = BASE_DIR
    project_name: str = Field(..., env='PROJECT_NAME')
    host: str = Field(..., env='APP_HOST')
    port: int = Field(..., env='APP_PORT')
    default_page_size: int = Field(..., env='DEFAULT_PAGE_SIZE')
    is_debug: bool = Field(..., env='IS_DEBUG')


class ElasticConfig(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')
    index_movies: str = Field(..., env='INDEX_MOVIES')
    index_person: str = Field(..., env='INDEX_PERSON')
    index_genre: str = Field(..., env='INDEX_GENRE')


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')
    password: str = Field(..., env='REDIS_PASSWORD')


class CacheTTLConfig(BaseSettings):
    default_ttl: int = 60 * 30
    movies_ttl: int = 60 * 5
    persons_ttl: int = 60 * 5
    genres_ttl: int = 60 * 5



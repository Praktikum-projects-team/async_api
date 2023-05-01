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

    class Config:
        case_sensitive = False
        env_file = "./.env"
        env_file_encoding = "utf-8"


class ElasticConfig(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')
    index_movies: str = Field(..., env='INDEX_MOVIES')
    index_person: str = Field(..., env='INDEX_PERSON')
    index_genre: str = Field(..., env='INDEX_GENRE')

    class Config:
        case_sensitive = False
        env_file = "./.env"
        env_file_encoding = "utf-8"


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')

    class Config:
        case_sensitive = False
        env_file = "./.env"
        env_file_encoding = "utf-8"

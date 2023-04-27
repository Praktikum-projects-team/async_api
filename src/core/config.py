import os
from logging import config as logging_config
from pydantic import BaseSettings, Field
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    project_name: str = Field(..., env='PROJECT_NAME')


class ElasticConfig(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    port: int = Field(..., env='ELASTIC_PORT')


class RedisConfig(BaseSettings):
    host: str = Field(..., env='REDIS_HOST')
    port: int = Field(..., env='REDIS_PORT')

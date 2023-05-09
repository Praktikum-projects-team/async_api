import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSettings(BaseSettings):
    es_host: str = Field(..., env='ELASTIC_HOST')
    es_port: int = Field(..., env='ELASTIC_PORT')
    es_id_field: str = 'id'

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    api_host: str = Field(..., env='API_HOST')
    api_port: int = Field(..., env='APP_PORT')


test_settings = TestSettings()
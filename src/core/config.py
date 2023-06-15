import os

from pydantic import BaseSettings, Field

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
    default_ttl: int = Field(..., env='DEFAULT_TTL')
    movies_ttl: int = Field(..., env='MOVIES_TTL')
    persons_ttl: int = Field(..., env='PERSONS_TTL')
    genres_ttl: int = Field(..., env='GENRES_TTL')


class AuthConfig(BaseSettings):
    host: str = Field(..., env='AUTH_HOST')
    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field(..., env='JWT_ALGORITHM')
from typing import Optional

from core.config import CacheTTLConfig
from db.fulltext.abstract_fulltext_search import AbstractFulltextSearch
from models.base import BaseApiModel


class BaseFulltextIndex:

    def __init__(self, searcher: AbstractFulltextSearch, index_name: str, cache_ttl: Optional[int] = None):
        self.searcher = searcher
        self.index_name = index_name
        self.cache_ttl_in_seconds = cache_ttl or CacheTTLConfig().default_ttl

    @property
    def model(self) -> type(BaseApiModel):
        raise NotImplementedError

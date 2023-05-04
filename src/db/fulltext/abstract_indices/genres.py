import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import AbstractFulltextIndex
from models.genre import Genre


class AbstractGenreIndex(abc.ABC, AbstractFulltextIndex):
    @property
    def model(self) -> type(Genre):
        return Genre

import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.genre import Genre


class AbstractGenreIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Genre):
        return Genre

import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import AbstractFulltextIndex
from models.person import Person


class AbstractPersonIndex(abc.ABC, AbstractFulltextIndex):
    @property
    def model(self) -> type(Person):
        return Person

import abc
from typing import Any, Optional

from elasticsearch import NotFoundError

from db.fulltext.abstract_indices.base_index import BaseFulltextIndex
from models.person import Person


class AbstractPersonIndex(abc.ABC, BaseFulltextIndex):
    @property
    def model(self) -> type(Person):
        return Person

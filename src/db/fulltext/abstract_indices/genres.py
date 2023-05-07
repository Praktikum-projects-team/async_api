from db.fulltext.abstract_indices.base_index import AbstractFulltextIndex
from models.genre import Genre


class AbstractGenreIndex(AbstractFulltextIndex):
    @property
    def model(self) -> type(Genre):
        return Genre

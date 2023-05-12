import os


class EsIndex:
    MOVIES = 'movies'
    PERSON = 'person'
    GENRE = 'genre'


class Sort:
    DESC = '-imdb_rating'
    ASC = 'imdb_rating'


CACHE_TTL = int(os.getenv('DEFAULT_TTL'))
DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE'))

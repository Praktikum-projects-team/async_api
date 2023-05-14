import uuid
import random


async def get_films_data(n: int) -> list[dict]:
    genre_uuid = str(uuid.uuid4())
    return [{
        'id': str(uuid.uuid4()),
        'imdb_rating': round(random.uniform(3, 10), 1),
        'genre': [
            {'id': genre_uuid, 'name': 'Action'},
            {'id': str(uuid.uuid4()), 'name': 'Sci-Fi'}
        ],
        'title': 'The Star',
        'description': 'New World, new star',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': str(uuid.uuid4()), 'name': 'Ann'},
            {'id': str(uuid.uuid4()), 'name': 'Bob'}
        ],
        'writers': [
            {'id': str(uuid.uuid4()), 'name': 'Ben'},
            {'id': str(uuid.uuid4()), 'name': 'Howard'}
        ]
    } for _ in range(n)]


async def get_film_uuid_from_film_data(film_data: list[dict]) -> uuid:
    return film_data[0]['id']


async def get_genre_uuid_from_film_data(film_data: list[dict]) -> uuid:
    return film_data[0]['genre'][0]['id']

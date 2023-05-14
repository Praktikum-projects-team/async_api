import uuid


async def get_genres_data(n: int) -> list[dict]:
    return [{
        'id': str(uuid.uuid4()),
        'name': 'Action'
    } for _ in range(n)]


async def get_genre_uuid(genres: list[dict]):
    return genres[0]['id']

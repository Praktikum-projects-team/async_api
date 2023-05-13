import uuid


async def get_persons_data(n: int) -> list[dict]:
    return [{
        'id': str(uuid.uuid4()),
        'full_name': 'George Lucas',
        'films': [
            {
                'id': str(uuid.uuid4()),
                'role': ['Actor']
            },
            {
                'id': str(uuid.uuid4()),
                'role': ['Actor', 'Director']
            },
            {
                'id': str(uuid.uuid4()),
                'role': ['Director']
            },
            {
                'id': str(uuid.uuid4()),
                'role': ['Writer']
            }
        ]
    } for _ in range(n)]


async def get_person_uuid_from_person_data(person_data: list[dict]) -> uuid:
    return person_data[0]['id']

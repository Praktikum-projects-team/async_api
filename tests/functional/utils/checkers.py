from tests.functional.utils.constants import Sort


async def check_ratings(ratings: list[float], sort: str = Sort.DESC) -> None:
    if sort == Sort.DESC:
        assert all(ratings[i] >= ratings[i + 1] for i in range(len(ratings) - 1)), 'Ratings are not sorted desc'
    elif sort == Sort.ASC:
        assert all(ratings[i] <= ratings[i + 1] for i in range(len(ratings) - 1)), 'Ratings are not sorted asc'

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from services.genre import GenreService, get_genre_service
from api.v1.models.genres import GenreApi, genre_to_api
from api.v1.utils import Page
from typing import Optional

router = APIRouter()


@router.get('', response_model=list[GenreApi])
async def genre_list(genre_service: GenreService = Depends(get_genre_service),
                     page: Page = Depends()) -> list[GenreApi]:
    genres = await genre_service.get_genre_list(page)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    genres_list = [genre_to_api(genre) for genre in genres]
    return genres_list


@router.get('/search', response_model=list[GenreApi])
async def genre_search(
        query: Optional[str] = Query(
            ...,
            title='Query field',
            description='Query field (search by genres name)'
        ),
        genre_service: GenreService = Depends(get_genre_service),
        page: Page = Depends()
) -> list[GenreApi]:
    genres = await genre_service.search_genres(query, page)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    genres_list = [genre_to_api(genre) for genre in genres]
    return genres_list


@router.get('/{genre_id}', response_model=GenreApi)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreApi:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre_to_api(genre)

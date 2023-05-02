from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, UUID4
from services.genre import GenreService, get_genre_service
from src.models.genre import Genre

router = APIRouter()


# class Genre(BaseModel):
#     uuid: UUID4
#     name: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return Genre(uuid=genre.uuid, name=genre.name)


@router.get('/', response_model=list[Genre])
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genres = await genre_service.get_genre_list()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
    genres_list = []
    for genre in genres:
        genres_list.append(Genre(uuid=genre.uuid, name=genre.name))
    return genres_list

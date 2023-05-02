from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class FilmBase(BaseModel):
    id: str
    title: str


@router.get('/{film_id}', response_model=FilmBase)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmBase:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmBase(id=film.id, title=film.title)

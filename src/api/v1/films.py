from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


class FilmEndpoint(Film):
    pass


@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmEndpoint:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmEndpoint(
        id=film.id,
        title=film.title,
        imbd_rating=film.imdb_rating,
        description=film.description,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
        genre=film.genre,
    )

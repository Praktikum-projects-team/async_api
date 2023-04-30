from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.film import FilmBase
from api.v1.models_api import FilmDetails, FilmGenreFilter, FilmSort, Page
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmDetails,
    summary='Подробная информация о фильме',
    description='Вывод подробной информации по uuid фильма',
    response_description='uuid, название, рейтинг, описание, режиссеры, актеры, сценаристы, жанры'
)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetails:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetails(
        id=film.id,
        title=film.title,
        imbd_rating=film.imdb_rating,
        description=film.description,
        directors=film.directors,
        actors=film.actors,
        writers=film.writers,
        genre=film.genre,
    )


@router.get(
    '',
    response_model=list[FilmBase],
    summary='Список фильмов',
    description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по рейтингу',
    response_description='uuid, название и рейтинг'
)
async def get_all_film(
    genre_filter: FilmGenreFilter = Depends(),
    sort: FilmSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmBase]:
    films = await film_service.get_all_films(sort.sort, page.page_size, page.page_number, genre_filter.genre_filter)
    return films

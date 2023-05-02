from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models_api import (
    FilmBaseApi,
    FilmDetailsApi,
    FilmFilter,
    FilmQuery,
    FilmSort,
    Page,
    film_to_api,
    genre_to_api,
    person_to_api
)
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '',
    response_model=list[FilmBaseApi],
    summary='Список фильмов',
    description='Список фильмов с пагинацией, фильтрацией по жанрам и сортировкой по рейтингу',
    response_description='uuid, название и рейтинг'
)
async def get_all_films(
    filtration: FilmFilter = Depends(),
    sort: FilmSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> list[FilmBaseApi]:
    films = await film_service.get_all_films(sort.sort, page, filtration.genre)
    films_for_api = [film_to_api(film) for film in films]
    return films_for_api


@router.get(
    '/search',
    response_model=list[FilmBaseApi],
    summary='Поиск фильмов',
    description='Список фильмов, удовлетворяющих условию поиска',
    response_description='Фильмы с их uuid, названием и рейтингом'
)
async def search_film(
    query: FilmQuery = Depends(),
    page: Page = Depends(),
    sort: FilmSort = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> Optional[list[FilmBaseApi]]:
    films = await film_service.search_film(page, query.query, sort.sort)
    films_for_api = [film_to_api(film) for film in films]
    return films_for_api


@router.get(
    '/{film_id}',
    response_model=FilmDetailsApi,
    summary='Подробная информация о фильме',
    description='Вывод подробной информации по uuid фильма',
    response_description='uuid, название, рейтинг, описание, режиссеры, актеры, сценаристы, жанры'
)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> FilmDetailsApi:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetailsApi(
        uuid=film.id,
        title=film.title,
        imbd_rating=film.imdb_rating,
        description=film.description,
        directors=[person_to_api(director) for director in film.directors],
        actors=[person_to_api(actor) for actor in film.actors],
        writers=[person_to_api(writer) for writer in film.writers],
        genre=[genre_to_api(genre) for genre in film.genre],
    )

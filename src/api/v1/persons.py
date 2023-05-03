from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, UUID4, Field
from services.person import PersonService, get_person_service
from services.film import FilmService, get_film_service
from typing import Optional
from src.models.film import FilmBase
from src.models.person import PersonBase, PersonFilms
from api.v1.models_api import (
    FilmPersonApi, PersonApi, FilmFilter, FilmSort, FilmBaseApi, person_to_api_detail,
    film_to_api, Page)

router = APIRouter()


@router.get('/', response_model=list[PersonApi])
async def person_list(person_service: PersonService = Depends(get_person_service), page: Page = Depends()) -> list[
    PersonApi]:
    persons = await person_service.get_persons_list(page)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    persons_list = [person_to_api_detail(person) for person in persons]
    return persons_list


@router.get('/search', response_model=list[PersonApi])
async def search_persons(
        query: Optional[str] = Query(
            ...,
            title='Query field',
            description='Query field (search by persons full_name)'
        ),
        person_service: PersonService = Depends(get_person_service),
        page: Page = Depends()) -> list[PersonApi]:
    persons = await person_service.search_persons(query, page)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    persons_list = [person_to_api_detail(person) for person in persons]
    return persons_list


@router.get('/{person_id}', response_model=PersonApi)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonBase:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return person_to_api_detail(person)


@router.get('/{person_id}/film', response_model=list[FilmBaseApi])
async def person_film(person_id: str, filtration: FilmFilter = Depends(), sort: FilmSort = Depends(),
                      film_service: FilmService = Depends(get_film_service),
                      page: Page = Depends()) -> list[FilmBaseApi]:
    filtration.person = person_id
    person_films = await film_service.get_films_by_person(sort.sort, page, filtration.person)
    if not person_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person films not found')
    person_films_for_api = [film_to_api(film) for film in person_films]
    return person_films_for_api

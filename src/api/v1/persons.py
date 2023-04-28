from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, UUID4, Field
from services.genre import PersonService, get_person_service
from typing import Optional

router = APIRouter()


class PersonFilms(BaseModel):
    roles: list[str]
    uuid: UUID4


class Person(BaseModel):
    uuid: UUID4
    full_name: str
    films: Optional[list[PersonFilms]] = Field(default_factory=list)


@router.get('/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')
    return Person(uuid=person.id, name=person.title)


@router.get('/', response_model=list[Person])
async def person_list(person_service: PersonService = Depends(get_person_service)) -> list[Person]:
    persons = await person_service.get_list()
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='persons not found')
    persons_list = []
    for person in persons:
        persons_list.append(Person(uuid=person.id, name=person.title))
    return persons_list

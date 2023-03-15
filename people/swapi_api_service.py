import asyncio
import logging
import math
from dataclasses import dataclass
from datetime import date
from typing import (
    Any,
    Coroutine,
)

from httpx import (
    AsyncClient,
)

from project_config.settings import (
    SWAPI_PEOPLE_URL,
    SWAPI_PLANET_URL,
)

logger = logging.Logger('main')

PAGINATION_SWAPI_LIMIT = 10


@dataclass(slots=True, frozen=True)
class Person:
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    date: date


def create_tasks(client: AsyncClient, url: str, total_pages: int) -> list[Coroutine]:
    tasks = []
    for page in range(2, total_pages + 1):
        tasks.append(client.get(f'{url}?page={page}'))

    return tasks


async def get_entity_data(url: str) -> list[dict[str, Any]]:
    async with AsyncClient() as client:
        entity_data = []
        try:
            response = await client.get(f'{url}?page=1')
            if response.status_code == 200 and response.json().get('count'):
                entity_data.extend(response.json()['results'])
                total_pages = math.ceil((response.json().get('count')/PAGINATION_SWAPI_LIMIT))
                tasks = create_tasks(client, url, total_pages)
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    entity_data.extend(response.json()['results'])
                return entity_data
            else:
                return []

        except RuntimeError:
            return []


async def get_api_data() -> tuple[Any, Any]:
    ''' Create tasks for necessary data '''
    async with asyncio.TaskGroup() as task_group:
        task_people = task_group.create_task(get_entity_data(SWAPI_PEOPLE_URL))
        task_planet = task_group.create_task(get_entity_data(SWAPI_PLANET_URL))
    return task_people.result(), task_planet.result()


async def get_swapi_response() -> list[Person]:
    try:
        peoples, planets = await get_api_data()
        return _parse_people_results(peoples, planets)
    except Exception as e:
        print(e.with_traceback())
        logger.error('didn\'t manage to connect to SWAPI')
        return []


def _parse_people_results(peoples: list[dict[str, Any]], planets: list[dict[str, Any]]) -> list[Person]:
    persons = []
    planets_mapping = {}

    for planet in planets:
        planets_mapping[planet['url']] = planet['name']

    for item in peoples:
        person = Person(
            name=item['name'],
            height=item['height'],
            mass=item['mass'],
            hair_color=item['hair_color'],
            skin_color=item['skin_color'],
            eye_color=item['eye_color'],
            birth_year=item['birth_year'],
            gender=item['gender'],
            homeworld=planets_mapping.get(item['homeworld']),
            date=date.today()
        )
        persons.append(person)
    return persons

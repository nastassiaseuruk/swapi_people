import logging
import math
import os
import uuid

import petl
from asgiref.sync import (
    sync_to_async,
)
from dataclass_csv import DataclassWriter
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render

from people.models import Collection
from people.swapi_api_service import (
    get_swapi_response,
    Person,
)
from project_config.settings import PAGINATION_LIMIT


async def load_collection(request: HttpRequest) -> HttpResponse:
    try:
        people_data = await get_swapi_response()
        if people_data:
            new_collection = Collection()
            with open(f'{os.getcwd()}/people/files/csv/{new_collection.id}.csv', 'w') as f:
                w = DataclassWriter(f, people_data, Person)
                w.write()
            await sync_to_async(new_collection.save)()
            return HttpResponse(200)
        else:
            return HttpResponse(400)

    except Exception:
        print('Gave up waiting, task canceled')
        return HttpResponse(400)


def list_collections(request: HttpRequest) -> HttpResponse:
    collections = Collection.objects.all().order_by('-date_created')
    return render(request, 'base.html', {'collections': collections})


def get_collection(request: HttpRequest, collection_uuid: uuid.UUID) -> HttpResponse:
    filename = f'{os.getcwd()}/people/files/csv/{collection_uuid}.csv'
    file = petl.fromcsv(filename)

    page = int(request.GET.get('page', 1))
    people_table = petl.head(file, page*PAGINATION_LIMIT)

    data = {"table": petl.toarray(people_table), 'file_name': collection_uuid}

    next_page = page + 1 if page < math.ceil(len(file)/PAGINATION_LIMIT) else None
    if next_page:
        data.update({'next_page': next_page})

    return render(request, "detail.html", data)


def get_collection_value_count(request: HttpRequest, collection_uuid: uuid.UUID) -> HttpResponse:
    filename = f'{os.getcwd()}/people/files/csv/{collection_uuid}.csv'
    people_table = petl.fromcsv(filename)

    fields = request.GET.get('fields')
    if not fields:
        return HttpResponse(400)

    aggregated = petl.aggregate(people_table, key=tuple(request.GET.get('fields').split(',')), aggregation=len)
    data = {"table": petl.toarray(aggregated), 'file_name': collection_uuid, 'headers': petl.header(aggregated)}

    return render(request, "value_count.html", data)

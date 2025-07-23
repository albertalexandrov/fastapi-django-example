from fastapi import Query
from fastapi_django.db.services.list import FilterSet, Ordering
from pydantic import Field


class UsersFilterSet(FilterSet):
    # TODO: не смог сделать вложенные фильтры
    name__ilike: str | None = Query(None)
    role_id: int | None = Query(None)
    role__code__in: list[str] | None = Field(Query(None, alias="role__code"))  # нужно именно прописывать Field(Query(...)), чтобы корректно отображалось в сваггере


class UsersOrdering(Ordering):
    ordering: list[str] = Field(Query(["id"]))  # нужно именно прописывать Field(Query(...)), чтобы корректно отображалось в сваггере

from typing import Any, Self

from fastapi import Depends
from kz.auth.usr_adm import User as RequestUser
from fastapi_django.db.repositories.queryset import QuerySet
from fastapi_django.db.services.list import ListService, LimitOffsetPagination
from fastapi_django.exceptions import HTTP400Exception
from starlette.requests import Request

from models import User
from shared.repositories import UserRolesRepository, UsersRepository
from web.api.crud.filtersets import UsersFilterSet, UsersOrdering


class RoleNotFoundHTTPException(HTTP400Exception):
    def __init__(self, headers: dict | None = None) -> None:
        super().__init__(detail="Роль не найдена", headers=headers)


class CreateUserService:
    def __init__(self, users: UsersRepository = Depends(), user_roles: UserRolesRepository = Depends()):
        self._users = users
        self._user_roles = user_roles

    async def create_user(self, data: dict, user: RequestUser) -> User:
        data["created_by_email"] = user.username
        role_id = data.pop('role_id')
        if (role := await self._user_roles.get_by_pk(role_id)) is None:
            raise RoleNotFoundHTTPException
        data["role"] = role
        return await self._users.commit(True).create(**data)


class UsersListService(ListService):
    # реализация сервиса, который возвращает список пользователей
    # предоставляет возможности для фильтрации, пагинации, сортировки

    def __init__(self, users: UsersRepository, **kw: Any) -> None:
        super().__init__(**kw)
        self._users = users

    def get_queryset(self) -> QuerySet:
        return self._users.objects.all()

    @classmethod
    def init(
        cls,
        request: Request,
        users: UsersRepository = Depends(),
        filterset: UsersFilterSet = Depends(),
        ordering: UsersOrdering = Depends(),
        pagination: LimitOffsetPagination = Depends(),
    ) -> Self:
        # метод, который использует fastapi для инициализации сервиса
        return cls(request=request, users=users, filterset=filterset, ordering=ordering, pagination=pagination)

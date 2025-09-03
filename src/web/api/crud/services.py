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


class UserNotFoundHTTPException(HTTP400Exception):
    def __init__(self, user_id: int, headers: dict | None = None) -> None:
        super().__init__(detail=f"Пользователь id={user_id} не найден", headers=headers)


class UsersService:
    def __init__(self, users: UsersRepository = Depends(), user_roles: UserRolesRepository = Depends()):
        self._users = users
        self._user_roles = user_roles

    async def create_user(self, data: dict, user: RequestUser) -> User:
        data = await self._validate_data(data)
        data["created_by_email"] = user.username
        return await self._users.commit().create(**data)

    async def update_user(self, user_id: int, data: dict) -> User:
        if not (user := await self._users.get_by_pk(user_id)):
            raise UserNotFoundHTTPException(user_id)
        data = await self._validate_data(data)
        return user.update(**data)

    async def _validate_data(self, data: dict) -> dict:
        role_id = data.pop('role_id')
        if (role := await self._user_roles.get_by_pk(role_id)) is None:
            raise RoleNotFoundHTTPException
        data["role"] = role
        return data


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

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi_django.db.dependencies import contextify_autocommit_session, contextify_transactional_session
from fastapi_django.db.sessions import contextified_transactional_session
from fastapi_django.exceptions import HTTP404Exception
from kz.auth.usr_adm import UsrAdmAuth
from kz.permissions import CodenamePermission
from pydantic import BaseModel

from shared.repositories import UsersRepository
from web.api.crud.services import UsersService, UsersListService

router = APIRouter(tags=["Примеры CRUD операций"])

CanCreateOffer = CodenamePermission("offer_create")
UserNotFoundHTTPException = HTTP404Exception("Пользователь не найден")


@router.get(
    "/simple/get/user/{user_id}",
    description="Пример простого get запрос (сложный - с фильтрами, сортировками и пагинацией)",
    dependencies=[
        Depends(UsrAdmAuth()),
        Depends(CanCreateOffer),
        Depends(contextify_autocommit_session())
    ]
)
async def simple_get(request: Request, user_id: int, users: UsersRepository = Depends()):
    # с простыми get запросами проблем быть не должно.  думаю, в большинстве случаев, будет достаточно
    # функционала кверисетов.  а если не хватит, то скорее всего можно будет обойтись один созданным
    # методом в репозитории.  создание отдельного сервис для get запроса - крайний случай
    print(f"Поступил запрос от пользователя {request.user.username}")
    if user := await users.objects.filter(id=user_id).first():
        return user
    raise UserNotFoundHTTPException


class UserCreateUpdateData(BaseModel):
    name: str
    role_id: int


@router.post(
    "/user/create",
    description="Пример создания объекта",
    dependencies=[
        Depends(UsrAdmAuth()),
        Depends(CanCreateOffer),
        Depends(contextify_transactional_session())
    ]
)
async def create_user(request: Request, data: UserCreateUpdateData, service: Annotated[UsersService, Depends()]):
    return await service.create_user(data.model_dump(), request.user)


@router.put(
    "/user/{user_id}/update",
    description="Пример обновления объекта",
    dependencies=[
        # Depends(UsrAdmAuth()),
        # Depends(CanCreateOffer),
    ]
)
async def update_user(user_id: int, data: UserCreateUpdateData, service: Annotated[UsersService, Depends()]):
    async with contextified_transactional_session():
        return await service.update_user(user_id, data.model_dump())


@router.get(
    "/filtering-ordering-paginate-users",
    dependencies=[Depends(contextify_autocommit_session())]
)
async def get_users(service: UsersListService = Depends(UsersListService.init)):
    return await service.list()

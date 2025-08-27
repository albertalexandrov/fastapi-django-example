from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi_django.db.dependencies import contextify_autocommit_session
from fastapi_django.exceptions import HTTP404Exception
from kz.auth.usr_adm import UsrAdmAuth
from kz.permissions import CodenamePermission
from pydantic import BaseModel

from shared.repositories import UsersRepository
from web.api.crud.services import CreateUserService, UsersListService

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


class UserCreateData(BaseModel):
    name: str
    role_id: int


@router.post(
    "/create/user",
    description="Пример создания объекта",
    dependencies=[
        Depends(UsrAdmAuth()),
        Depends(CanCreateOffer),
        Depends(contextify_autocommit_session())
    ]
)
async def create_user(request: Request, data: UserCreateData, service: Annotated[CreateUserService, Depends()]):
    return await service.create_user(data.model_dump(), request.user)


@router.get(
    "/filtering-ordering-paginate-users",
    dependencies=[Depends(contextify_autocommit_session())]
)
async def get_users(service: UsersListService = Depends(UsersListService.init)):
    return await service.list()

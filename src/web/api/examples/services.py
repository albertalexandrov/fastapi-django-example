from fastapi import APIRouter, Depends, Request
from fastapi_django.auth.some_kz_lib.usr_adm_auth import UsrAdmAuth
from fastapi_django.db.dependencies import contextify_autocommit_session
from fastapi_django.exceptions.http import HTTP401Exception, HTTP404Exception
from fastapi_django.permissions.some_kz_lib.permissions import CodenamePermission

from web.dependencies import UsersRepository

router = APIRouter(tags=["Примеры сервисов"])

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
async def simple_get(request: Request, user_id: int, users: UsersRepository):
    # с простыми get запросами проблем быть не должно.  думаю, в большинстве случаев, будет достаточно
    # функионала кверисетов.  а если не хватит, то скорее всего можно будет обойтись один созданным
    # методом в репозитории.  создание отдельного сервис для get запроса - крайний случай
    print(f"Поступил запрос от пользователя {request.user.username}")
    if user := await users.objects.filter(id=user_id).first():
        return user
    raise UserNotFoundHTTPException

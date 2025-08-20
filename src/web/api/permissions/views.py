from fastapi import APIRouter, Depends
from fastapi_django.permissions import PermissionClasses
from fastapi_django.permissions.some_kz_lib.permissions import CodenamePermission
from kz.auth.usr_adm import UsrAdmAuth
from starlette.requests import Request

router = APIRouter(tags=["Примеры работы с пермишенами"])

# можно каждый раз определять пермишен в виде CodenamePermission("offer_create"),
# а можно дальнейшего переиспользования так:
CanCreateOffer = CodenamePermission("offer_create")


@router.get(
    "/codename-permission",
    description="Пример использования пермишена CodenamePermission",
    dependencies=[
        Depends(UsrAdmAuth()),  # сначала аутентифицируем
        Depends(CanCreateOffer),
    ]
)
async def custom_permissions(request: Request):
    print(request.user)


@router.get(
    "/multiple-permissions",
    description="Пример проверки нескольких пермишенов",
    dependencies=[Depends(PermissionClasses(CanCreateOffer, CodenamePermission("DOES NOT EXIST")))]
)
async def multiple_permissions(request: Request):
    print(request.user)

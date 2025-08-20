from fastapi import APIRouter, Depends
from fastapi_django.permissions import PermissionClasses
from kz.auth.usr_adm import UsrAdmAuth
from kz.permissions import CodenamePermission
from starlette.requests import Request

router = APIRouter(tags=["Примеры работы с пермишенами"])

# можно каждый раз определять пермишен в виде CodenamePermission("partners_edit"),
# а можно дальнейшего переиспользования так:
CanEditPartners = CodenamePermission("partners_edit")
# ну или вообще вынести в таком виде библиотеку


@router.get(
    "/codename-permission",
    description="Пример использования пермишена CodenamePermission",
    dependencies=[
        Depends(UsrAdmAuth()),  # сначала аутентифицируем
        Depends(CanEditPartners),
    ]
)
async def custom_permissions(request: Request):
    return request.user.model_dump()


@router.get(
    "/multiple-permissions",
    description="Пример проверки нескольких пермишенов",
    dependencies=[
        Depends(UsrAdmAuth()),
        Depends(PermissionClasses(CanEditPartners, CodenamePermission("DOES NOT EXIST")))
    ]
)
async def multiple_permissions(request: Request):
    return request.user.model_dump()

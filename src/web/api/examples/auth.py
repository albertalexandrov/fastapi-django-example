from fastapi import APIRouter, Depends
from fastapi_django.auth import CredentialsBasicAuthentication, AuthenicationClasses
from fastapi_django.auth.some_kz_lib.usr_adm_auth import UsrAdmAuth
from fastapi_django.conf import settings
from starlette.requests import Request

from web.auth import ServiceUserAuth

router = APIRouter(tags=["Примеры аутентификации"])


@router.get(
    "/multiple-auth-schemes",
    description="Пример эндпойнта, в котором можно аутентифицироваться двумя способами",
    dependencies=[
        Depends(AuthenicationClasses(ServiceUserAuth(auto_error=False), UsrAdmAuth(auto_error=False))),
    ]
)
async def multiple_schemes(request: Request):
    print(request.user)


@router.get(
    "/service-user-auth",
    description=(
        "Аутентификация сервисного пользователя, "
        "информация о котором (логин, пароль) хранится в модели SQLAlchemy"
    ),
    dependencies=[
        Depends(ServiceUserAuth()),
    ]
)
async def service_user_auth(request: Request):
    print(request.user)


@router.get(
    "/credentials-basic-auth",
    description="Пример базовой аутентификации, при которой происходит сравнение полученных кредов с заданными",
    dependencies=[
        Depends(CredentialsBasicAuthentication(settings.INTEGRATION_USER_USERNAME, settings.INTEGRATION_USER_PASSWORD))
    ]
)
async def credentials_basic_auth(request: Request):
    print(request.user)


@router.get(
    "/usr-adm-auth",
    description="Пример кастомной аутентификации",
    dependencies=[
        Depends(UsrAdmAuth()),
    ]
)
async def usr_adm_auth(request: Request):
    print(request.user)

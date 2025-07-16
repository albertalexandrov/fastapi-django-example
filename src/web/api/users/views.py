
from fastapi import APIRouter, Depends
from fastapi_django.auth import AuthenticationClasses
from fastapi_django.auth.some_kz_lib.usr_adm import UsrAdmAuth
from fastapi_django.db.dependencies import contextify_autocommit_session, ContextifiedAutocommitSession
from fastapi_django.db.sessions import contextified_autocommit_session
from fastapi_django.permissions import PermissionClasses
from fastapi_django.permissions.some_kz_lib.permissions import CodenamePermission
from sqlalchemy import select
from starlette.requests import Request

from models import User
from shared.repositories.users import UsersRepository

router = APIRouter()


@router.get(
    "/users",
    dependencies=[
        Depends(contextify_autocommit_session()),
        Depends(AuthenticationClasses(UsrAdmAuth())),
        Depends(PermissionClasses(CodenamePermission("offer_create"), CodenamePermission("bad_codename"))),
    ]
)
async def get_users(
    request: Request, repository: UsersRepository = Depends()
):
    print("user ===> ", request.user)
    user = await repository.flush().create(name="ASCGVHASG")
    print(user)
    return user


@router.get(
    "/custom-auth",
    description="Пример кастомной аутентификации",
    dependencies=[
        Depends(AuthenticationClasses(UsrAdmAuth())),
    ]
)
async def custom_auth(request: Request):
    print("user ===> ", request.user)


@router.get(
    "/custom-permissions",
    dependencies=[
        Depends(AuthenticationClasses(UsrAdmAuth())),  # сначала аутентифицируем
        Depends(PermissionClasses(CodenamePermission("offer_create"), CodenamePermission("bad_codename"))),
    ]
)
async def custom_permissions(request: Request):
    print("user ===> ", request.user)


@router.get(
    "/contextify-autocommit-session",
    description="Пример с использованием зависимости contextify_autocommit_session()",
    dependencies=[
        Depends(contextify_autocommit_session()),
    ]
)
async def contextify_autocommit_session(repository: UsersRepository = Depends()):
    return await repository.objects.all()


@router.get(
    "/contextified-autocommit-session-annotated",
    description="Пример с использование типа ContextifiedAutocommitSession",
)
async def contextified_autocommit_session_annotated(session: ContextifiedAutocommitSession):
    stmt = select(User)
    result = await session.scalars(stmt)
    return result.all()


@router.get(
    "/contextified-autocommit-session-context-manager",
    description="Пример использования контекстного менеджера contextified_autocommit_session()"
)
async def contextified_autocommit_session_context_manager():
    async with contextified_autocommit_session() as session:
        stmt = select(User)
        result = await session.scalars(stmt)
        users1 = result.all()
        print("users1", users1)
        repository = UsersRepository()
        users2 = await repository.objects.all()
        print("users2", users2)

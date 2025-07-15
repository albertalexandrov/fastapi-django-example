
from fastapi import APIRouter, Depends
from fastapi_django.auth.some_kz_lib.dependencies import AdmUsr
from fastapi_django.auth.some_kz_lib.usr_adm import UsrAdmAuth
from fastapi_django.db.dependencies import (
    contextify_autocommit_session,
)

from shared.repositories.users import UsersRepository

router = APIRouter()


@router.get(
    "/users",
    dependencies=[
        Depends(contextify_autocommit_session()),
        # Depends(UsrAdmAuth()),
    ]
)
async def get_users(
    user: AdmUsr,
    repository: UsersRepository = Depends()
):
    print("user ===> ", user)
    user = await repository.flush().create(name="ASCGVHASG")
    print(user)
    return user


# @router.get("/bare-session")
# async def test_bare_session(session: ContextifiedAutocommitSession):
#     # пример использования типа ContextifiedAutocommitSession
#     return await session.scalar(text("SELECT 1"))

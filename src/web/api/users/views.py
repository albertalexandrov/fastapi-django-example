from fastapi import APIRouter, Depends
from fastapi_django.auth.some_kz_lib.usr_adm_auth import UsrAdmAuth
from fastapi_django.db.dependencies import contextify_autocommit_session
from starlette.requests import Request

from shared.repositories.users import UsersRepository

router = APIRouter()


@router.get(
    "/users",
    dependencies=[
        Depends(UsrAdmAuth()),
        Depends(contextify_autocommit_session()),
    ]
)
async def get_users(
    request: Request, repository: UsersRepository = Depends()
):
    print("user ===> ", request.user)
    user = await repository.flush().create(name="ASCGVHASG")
    print(user)
    return user

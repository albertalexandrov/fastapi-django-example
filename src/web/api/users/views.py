from fastapi import APIRouter, Depends
from fastapi_django.db.dependencies import (
    contextify_autocommit_session,
    ContextifiedAutocommitSession,
)
from sqlalchemy import text

from shared.repositories.users import UsersRepository

router = APIRouter()


@router.get("/users", dependencies=[Depends(contextify_autocommit_session())])
async def get_users(repository: UsersRepository = Depends()):
    user = await repository.flush().create(name="ASCGVHASG")
    print(user)
    return user


@router.get("/bare-session")
async def test_bare_session(session: ContextifiedAutocommitSession):
    # пример использования типа ContextifiedAutocommitSession
    return await session.scalar(text("SELECT 1"))

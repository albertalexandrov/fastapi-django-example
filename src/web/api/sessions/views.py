from fastapi import APIRouter, Depends
from fastapi_django.db.dependencies import contextify_autocommit_session, ContextifiedAutocommitSession
from fastapi_django.db.sessions import contextified_autocommit_session
from sqlalchemy import select

from models import User
from shared.repositories.users import UsersRepository

router = APIRouter(tags=["Примеры работы с сессиями SQLAlchemy"])


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

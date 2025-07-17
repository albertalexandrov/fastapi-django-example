from fastapi.security import HTTPBasicCredentials
from fastapi_django.auth import BasicAuthentication
from fastapi_django.db.sessions import contextified_autocommit_session

from models import ServiceUser
from shared.repositories.service import ServiceUsersRepository


class ServiceUserAuth(BasicAuthentication):
    """
    Аутентификация по модели пользователя, которая может быть только в сервисе, в котором используется,
    ее невозможно вынести в библиотеку, тк модель пользователя может быть где угодно и поля с username
    и password тоже может быть где угодно.  Также может потребоваться какая нибудь дополнительная логика,
    например, отфильтровать только активным пользователей
    """
    async def _authenticate(self, credentials: HTTPBasicCredentials | None) -> ServiceUser | None:
        if credentials is None:
            return None
        async with contextified_autocommit_session():
            service_users = ServiceUsersRepository()
            user = await service_users.active.filter(username=credentials.username).first()
            if user is None:
                return
            if user.password == credentials.password:
                return user

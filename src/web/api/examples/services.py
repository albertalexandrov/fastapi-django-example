from fastapi_django.auth.some_kz_lib.usr_adm_auth import User as RequestUser
from fastapi_django.exceptions.http import HTTP400Exception

from models import User
from shared.repositories import UsersRepository, UserRolesRepository


class RoleNotFoundHTTPException(HTTP400Exception):

    def __init__(self, headers: dict | None = None) -> None:
        super().__init__(detail="Роль не найдена", headers=headers)


class CreateUserService:
    def __init__(self):
        self._users_repository = UsersRepository()
        self._user_roles_repository = UserRolesRepository()

    async def create_user(self, data: dict, user: RequestUser) -> User:
        data["created_by_email"] = user.username
        role_id = data.pop('role_id')
        if (role := await self._user_roles_repository.get_by_pk(role_id)) is None:
            raise RoleNotFoundHTTPException
        data["role"] = role
        return await self._users_repository.commit(True).create(**data)

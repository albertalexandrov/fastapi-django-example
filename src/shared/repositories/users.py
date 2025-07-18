from fastapi_django.db.repositories.base import BaseRepository

from models import User, UserRole


class UsersRepository(BaseRepository):
    model_cls = User


class UserRolesRepository(BaseRepository):
    model_cls = UserRole
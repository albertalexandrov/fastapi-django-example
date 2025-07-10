from fastapi_django.db.repositories.base import BaseRepository

from models import User


class UsersRepository(BaseRepository):
    model_cls = User

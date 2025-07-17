from fastapi_django.db.repositories import BaseRepository
from fastapi_django.db.repositories.queryset import QuerySet

from models import ServiceUser


class ServiceUsersRepository(BaseRepository):
    model_cls = ServiceUser

    @property
    def active(self) -> QuerySet:
        return self.objects.filter(is_active=True)

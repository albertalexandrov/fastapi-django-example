from fastapi_django.db.models.base import Model
from sqlalchemy.orm import Mapped, mapped_column


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

from fastapi_django.db.models.base import Model
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String


class ServiceUser(Model):
    __tablename__ = "service_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(length=16), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(length=16))
    role: Mapped[str] = mapped_column(String(length=32))
    is_active: Mapped[bool] = mapped_column(default=True)

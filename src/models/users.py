from fastapi_django.db.models.base import Model
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(Model):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    role_id: Mapped[int | None] = mapped_column(ForeignKey("user_roles.id"))
    role: Mapped["UserRole"] = relationship(back_populates="users")
    created_by_email: Mapped[str | None] = mapped_column()

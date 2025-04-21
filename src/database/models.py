from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at, int_null, int_pk, str_nullable, str_uniq


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]
    hash_password: Mapped[str_nullable]
    vk: Mapped["UserVkModel"] = relationship(
        "UserVkModel",
        back_populates="user",
        uselist=False,
    )
    yandex: Mapped["UserYandexModel"] = relationship(
        "UserYandexModel",
        back_populates="user",
        uselist=False,
    )


class UserVkModel(Base):
    __tablename__ = "users_vk"
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    id_vk: Mapped[int_null]
    email: Mapped[str_uniq]
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="vk",
        uselist=False,
    )


class UserYandexModel(Base):
    __tablename__ = "users_yandex"
    id: Mapped[int_pk]
    created_at: Mapped[created_at]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    id_yandex: Mapped[str_uniq]
    login: Mapped[str_nullable]
    email: Mapped[str_uniq]
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="yandex",
        uselist=False,
    )

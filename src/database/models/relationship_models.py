from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.data import Base, int_null, int_pk, str_nullable, str_uniq


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]
    hash_password: Mapped[str_nullable]
    vk: Mapped["UserVk"] = relationship(
        "UserVk",
        back_populates="user",
        uselist=False,
    )
    yandex: Mapped["UserYandex"] = relationship(
        "UserYandex",
        back_populates="user",
        uselist=False,
    )
    mail_ru: Mapped["UserMailRu"] = relationship(
        "UserMailRu",
        back_populates="user",
        uselist=False,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r})"
        )

    def __repr__(self):
        return str(self)


class UserVk(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    id_vk: Mapped[int_null]
    email: Mapped[str_uniq]
    user: Mapped["User"] = relationship(
        "User",
        back_populates="vk",
        uselist=False,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r})"
        )

    def __repr__(self):
        return str(self)


class UserYandex(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    id_yandex: Mapped[str_uniq]
    login: Mapped[str_nullable]
    email: Mapped[str_uniq]
    user: Mapped["User"] = relationship(
        "User",
        back_populates="yandex",
        uselist=False,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r})"
        )

    def __repr__(self):
        return str(self)


class UserMailRu(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    id_mail_ru: Mapped[str_uniq]
    email: Mapped[str_uniq]
    user: Mapped["User"] = relationship(
        "User",
        back_populates="mail_ru",
        uselist=False,
    )

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r})"
        )

    def __repr__(self):
        return str(self)

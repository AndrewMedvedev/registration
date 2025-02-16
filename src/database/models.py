from sqlalchemy.orm import Mapped

from src.database.data import Base, int_null, int_pk, str_nullable, str_uniq


class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]
    hash_password: Mapped[str_nullable]

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
    id_vk: Mapped[int_null]
    email: Mapped[str_uniq]

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
    id_mail_ru: Mapped[str_uniq]
    email: Mapped[str_uniq]
    birthday: Mapped[str | None]

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
    id_yandex: Mapped[str_uniq]
    login: Mapped[str_nullable]
    email: Mapped[str_uniq]

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r})"
        )

    def __repr__(self):
        return str(self)

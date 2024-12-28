from sqlalchemy.orm import Mapped
from src.database import Base, str_uniq, int_pk, str_nullable, int_null


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

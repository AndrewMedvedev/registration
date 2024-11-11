from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base, str_uniq, int_pk, str_null_true , str_nullable , str_def
   

class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    first_name_fa : Mapped[str_null_true]
    email: Mapped[str_uniq]
    hash_password : Mapped[str_nullable]
    snils : Mapped[str_null_true]
    faculty : Mapped[str_null_true]
    number_school: Mapped[str_null_true]
    class_school : Mapped[str_null_true]
    group : Mapped[str_null_true]

    
    
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")


    def __repr__(self):
        return str(self)
    

from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base, str_uniq, int_pk, str_null_true , str_nullable
   

class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    first_name: Mapped[str_nullable]
    last_name: Mapped[str_nullable]
    first_name_fa : Mapped[str]
    email: Mapped[str_uniq]
    hash_password : Mapped[str_nullable]
    snils : Mapped[str_uniq]
    faculty : Mapped[str_nullable]
    number_school: Mapped[str_nullable]
    class_school : Mapped[str_nullable]
    group : Mapped[str_nullable]

    
    
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")


    def __repr__(self):
        return str(self)
    

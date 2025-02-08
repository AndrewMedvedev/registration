from typing import Annotated
from sqlalchemy import BIGINT
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from src.config import get_db_url


DATABASE_URL = get_db_url()


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


int_pk = Annotated[int, mapped_column(primary_key=True)]
int_null = Annotated[int, mapped_column(nullable=False, unique=True)]
big_int_uniq = Annotated[int, mapped_column(BIGINT, nullable=True, unique=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_uniq_null = Annotated[str, mapped_column(unique=True, nullable=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_nullable = Annotated[str, mapped_column(nullable=False)]
str_def = Annotated[str, mapped_column(default=None)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

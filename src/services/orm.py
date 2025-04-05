import logging

from sqlalchemy import select

from src.database.models import User, UserMailRu, UserVk, UserYandex
from src.errors import DataBaseError
from src.interfaces import CRUDBase
from src.services.db import DatabaseSessionService

log = logging.getLogger(__name__)


class ORMService(DatabaseSessionService, CRUDBase):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def add_user(self, user) -> int:
        try:
            async with self.session() as session:
                session.add(user)
                await session.commit()
                await session.refresh(user)
            return user.id
        except DataBaseError:
            raise DataBaseError("add_user")

    async def get_user_email(
        self,
        email: str,
    ) -> dict:
        async with self.session() as session:
            user = await session.execute(select(User).where(User.email == email))
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_user_email")

    async def get_user_phone_number(
        self,
        phone_number: str,
    ) -> dict:
        async with self.session() as session:
            user = await session.execute(
                select(User).where(User.phone_number == phone_number)
            )
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_user_phone_number")

    async def get_user_email_vk(self, email: str) -> dict:
        async with self.session() as session:
            user = await session.execute(select(UserVk).where(UserVk.email == email))
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_user_email_vk")

    async def get_user_email_mail_ru(self, email: str) -> dict:
        async with self.session() as session:
            user = await session.execute(
                select(UserMailRu).where(UserMailRu.email == email)
            )
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_user_email_mail_ru")

    async def get_user_email_yandex(self, email: str) -> dict:
        async with self.session() as session:
            user = await session.execute(
                select(UserYandex).where(UserYandex.email == email)
            )
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_user_email_yandex")

    async def get_data(self, user_id: int) -> dict:
        async with self.session() as session:
            user = await session.execute(select(User).where(User.id == user_id))
            log.warning(user)
            if (data := user.scalar()) is not None:
                return data
            raise DataBaseError("get_data")

    async def get_number(self, phone_number: str) -> bool:
        async with self.session() as session:
            user = await session.execute(
                select(User).where(User.phone_number == phone_number)
            )
            log.warning(user)
            try:
                if user.scalar() is not None:
                    return True
                return False
            except Exception:
                return False

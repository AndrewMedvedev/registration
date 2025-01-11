from sqlalchemy import select
from src.services.db import DatabaseSessionService
from src.database.models import User, UserVk


class ORMService(DatabaseSessionService):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def add_user(self, user):
        async with self.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return {"message": 200}

    async def get_user_email(self, email: str, hash_password: str):
        async with self.session() as session:
            user = await session.execute(
                select(User).where(
                    User.email == email and User.hash_password == hash_password
                )
            )
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)

    async def get_user_phone_number(self, phone_number: str, hash_password: str):
        async with self.session() as session:
            user = await session.execute(
                select(User).where(
                    User.phone_number == phone_number
                    and User.hash_password == hash_password
                )
            )
        try:
            return user.scalar()
        except Exception as _ex:
            print(_ex)

    async def get_user_id_vk(self, id_vk: int):
        async with self.session() as session:
            user = await session.execute(select(UserVk).where(UserVk.id_vk == id_vk))
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)

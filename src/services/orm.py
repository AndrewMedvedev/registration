from sqlalchemy import select
from src.services.db import DatabaseSessionService
from src.auth.schemas import UserModel


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


    async def get_user(self,email: str ,hash_password: str) -> UserModel | None:
        async with self.session() as session:
            user = await session.execute(
                select(UserModel).where(UserModel.email == email,UserModel.hash_password == hash_password)
            )
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)
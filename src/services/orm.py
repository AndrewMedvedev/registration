from sqlalchemy import select
from src.services.db import DatabaseSessionService
from src.auth.models import Applicant, Schoolboy,Student


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


    async def get_user_applicant(self,email: str ,hash_password: str) -> Applicant | None:
        async with self.session() as session:
            user = await session.execute(
                select(Applicant).where(Applicant.email == email and Applicant.hash_password == hash_password)
            )
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)
                
                
    async def get_user_student(self,email: str ,hash_password: str) -> Student | None:
        async with self.session() as session:
            user = await session.execute(
                select(Student).where(Student.email == email and Student.hash_password == hash_password)
            )
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)
                
                
    async def get_user_schoolboy(self,email: str ,hash_password: str) -> Schoolboy | None:
        async with self.session() as session:
            user = await session.execute(
                select(Schoolboy).where(Schoolboy.email == email and Schoolboy.hash_password == hash_password)
            )
            try:
                return user.scalars().one()
            except Exception as _ex:
                print(_ex)
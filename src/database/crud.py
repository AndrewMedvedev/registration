from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.exc import DataError, IntegrityError, NoResultFound

from config import settings

from ..exeptions import BadRequestHTTPError, ExistsHTTPError, NotFoundHTTPError
from ..schemas import Codes, GetAdminResponse, GetUserResponse, UserDataResponse
from .models import AdminModel, UserModel, UserVkModel, UserYandexModel
from .session import SQLSessionService


class SQLAuthorization(SQLSessionService):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def create_user(self, model: UserModel) -> UUID:
        try:
            async with self.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return model.id
        except DataError:
            raise BadRequestHTTPError from None
        except IntegrityError:
            raise ExistsHTTPError from None

    async def create_admin(self, model: AdminModel) -> UUID:
        try:
            async with self.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return model.id
        except DataError:
            raise BadRequestHTTPError from None
        except IntegrityError:
            raise ExistsHTTPError from None

    async def get_user_email(self, email: str) -> dict:
        try:
            async with self.session() as session:
                data = await session.execute(
                    select(UserModel.hash_password, UserModel.id).where(UserModel.email == email)
                )
                result = data.mappings().first()
                if result is None:
                    raise BadRequestHTTPError("wrong email")
                return GetUserResponse(**result).to_dict()
        except DataError:
            raise BadRequestHTTPError from None

    async def get_admin_email(self, email: str) -> dict:
        try:
            async with self.session() as session:
                data = await session.execute(
                    select(AdminModel.hash_password, AdminModel.id).where(
                        AdminModel.email == email
                    )
                )
                result = data.mappings().first()
                if result is None:
                    raise BadRequestHTTPError("wrong email")
                return GetAdminResponse(**result).to_dict()
        except DataError:
            raise BadRequestHTTPError from None

    async def get_user_phone_number(self, phone_number: str) -> dict:
        try:
            async with self.session() as session:
                data = await session.execute(
                    select(UserModel.hash_password, UserModel.id).where(
                        UserModel.phone_number == phone_number
                    )
                )
                result = data.mappings().first()
                if result is None:
                    raise BadRequestHTTPError("wrong phone number")
                return GetUserResponse(**result).to_dict()
        except DataError:
            raise BadRequestHTTPError from None

    async def get_data(self, user_id: UUID) -> dict:
        try:
            async with self.session() as session:
                data = await session.execute(
                    select(UserModel.first_name, UserModel.last_name, UserModel.email).where(
                        UserModel.id == user_id
                    )
                )
                result = data.mappings().first()
                if result is not None:
                    return UserDataResponse(**result).to_dict()
                raise BadRequestHTTPError
        except DataError:
            raise BadRequestHTTPError from None

    async def get_number(self, phone_number: str) -> str:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserModel.id).where(UserModel.phone_number == phone_number)
                )
                return str(result.scalar_one())
        except NoResultFound:
            raise NotFoundHTTPError from None
        except DataError:
            raise BadRequestHTTPError from None

    async def replace_password(self, user_id: UUID, new_password: str) -> None:
        try:
            async with self.session() as session:
                obj = (
                    await session.execute(select(UserModel).where(UserModel.id == user_id))
                ).scalar()
                obj.hash_password = new_password
                await session.commit()
        except NoResultFound:
            raise NotFoundHTTPError from None


class SQLVK(SQLSessionService):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def create_user(self, model: UserVkModel) -> None:
        try:
            async with self.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
        except DataError:
            raise BadRequestHTTPError from None
        except IntegrityError:
            raise ExistsHTTPError from None

    async def get_user_email(self, email: str) -> UUID:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserVkModel.user_id).where(UserVkModel.email == email)
                )
                return result.scalar_one()
        except NoResultFound:
            raise NotFoundHTTPError from None
        except DataError:
            raise BadRequestHTTPError from None


class SQLYandex(SQLSessionService):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def create_user(self, model: UserYandexModel) -> None:
        try:
            async with self.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
        except DataError:
            raise BadRequestHTTPError from None
        except IntegrityError:
            raise ExistsHTTPError from None

    async def get_user_email(self, email: str) -> UUID:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserYandexModel.user_id).where(UserYandexModel.email == email)
                )
                return result.scalar_one()
        except NoResultFound:
            raise NotFoundHTTPError from None
        except DataError:
            raise BadRequestHTTPError from None


class RedisOtherAuth:
    def __init__(self):
        self.session = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )

    async def add_code(self, schema: Codes) -> None:
        await self.session.setex(name=schema.state, value=schema.code_verifier, time=120)

    async def get_code(self, key: str) -> str:
        result = await self.session.get(key)
        await self.session.delete(key)
        return result

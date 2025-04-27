from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import DataError, IntegrityError, NoResultFound

from ..exeptions import BadRequestHTTPError, ExistsHTTPError, NotFoundHTTPError
from ..schemas import GetUserResponse, UserDataResponse
from .models import UserModel, UserVkModel, UserYandexModel
from .session import DatabaseSessionService


class SQLAuthorization(DatabaseSessionService):
    def __init__(self) -> None:
        super().__init__()
        self.init()

    async def create_user(self, model: UserModel) -> int:
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
                result = await session.execute(
                    select(UserModel.hash_password, UserModel.id).where(UserModel.email == email)
                )
                if result is not None:
                    return GetUserResponse(**result.mappings().first()).to_dict()
                raise BadRequestHTTPError
        except DataError:
            raise BadRequestHTTPError from None

    async def get_user_phone_number(
        self,
        phone_number: str,
    ) -> dict:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserModel.hash_password, UserModel.id).where(
                        UserModel.phone_number == phone_number
                    )
                )
                if result is not None:
                    return GetUserResponse(**result.mappings().first()).to_dict()
                raise BadRequestHTTPError
        except DataError:
            raise BadRequestHTTPError from None

    async def get_data(self, user_id: int) -> dict:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserModel.first_name, UserModel.last_name, UserModel.email).where(
                        UserModel.id == user_id
                    )
                )
                if result is not None:
                    return UserDataResponse(**result.mappings().first()).to_dict()
                raise BadRequestHTTPError
        except DataError:
            raise BadRequestHTTPError from None

    async def get_number(self, phone_number: str) -> bool:
        try:
            async with self.session() as session:
                result = await session.execute(
                    select(UserModel.phone_number).where(UserModel.phone_number == phone_number)
                )
                number = result.scalar()
                if isinstance(number, str):
                    return True
        except DataError:
            return False
        else:
            return False


class SQLVK(DatabaseSessionService):
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
                result.scalar_one()
        except NoResultFound:
            raise NotFoundHTTPError from None
        except DataError:
            raise BadRequestHTTPError from None


class SQLYandex(DatabaseSessionService):
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

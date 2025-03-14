from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse

from src.database.schemas import GetUserEmail, GetUserPhoneNumber, UserModel


class BasicAuthorizationBase(ABC):

    @abstractmethod
    async def registration(
        self,
        model: UserModel,
    ) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login_email(
        self,
        model: GetUserEmail,
    ) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login_phone(
        self,
        model: GetUserPhoneNumber,
    ) -> JSONResponse:
        raise NotImplementedError

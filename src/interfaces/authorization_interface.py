from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse


class AuthorizationBase(ABC):

    @abstractmethod
    async def registration(self) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login_email(self) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login_phone(self) -> JSONResponse:
        raise NotImplementedError

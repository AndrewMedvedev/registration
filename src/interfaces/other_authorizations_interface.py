from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse


class OtherAuthorizationsBase(ABC):

    @abstractmethod
    async def link(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_token(self) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def registration(self) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login(self) -> JSONResponse:
        raise NotImplementedError

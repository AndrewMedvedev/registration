from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse


class ReUseBase(ABC):

    @staticmethod
    @abstractmethod
    async def link(
        setting: str,
        dictlink: dict,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_token(
        self,
        dictgetdata: dict,
    ) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def registration(
        self,
        user_model,
    ) -> JSONResponse:
        raise NotImplementedError

    @abstractmethod
    async def login(
        self,
        dictgetdatatoken: dict,
        stmt_get,
    ) -> JSONResponse:
        raise NotImplementedError

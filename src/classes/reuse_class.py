from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.services.orm import ORMService


class ReUse:

    def __init__(self, func=None):
        self.func = func

    @staticmethod
    async def link(setting: str, dictlink: dict) -> str:
        url = f"{setting}?{'&'.join([f'{k}={v}' for k, v in dictlink])}"
        return url

    async def get_token(self, dictgetdata: dict) -> JSONResponse:
        model = dictgetdata
        user = await self.func(model)
        return JSONResponse(content=user)

    @staticmethod
    async def registration(user_model) -> JSONResponse:
        user_id = await ORMService().add_user(user_model)
        data = {"user_id": user_id}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

    async def login(
        self,
        dictgetdatatoken: dict,
        stmt_get,
    ) -> JSONResponse:
        model = dictgetdatatoken
        user = await self.func(model)
        stmt = await stmt_get(user.get("email"))
        if stmt.email == user.get("email").lower():
            data = {"user_id": stmt.id}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

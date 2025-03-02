from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.services.orm import ORMService


class ReUse:

    def __init__(self, func=None):
        self.func = func
        self.orm = ORMService()
        self.jwt_create = JWTCreate

    @staticmethod
    async def link(setting: str, dictlink: dict) -> str:
        url = f"{setting}?{'&'.join([f'{k}={v}' for k, v in dictlink.items()])}"
        return url

    async def get_token(self, dictgetdata: dict) -> JSONResponse:
        return JSONResponse(content=await self.func(dictgetdata))

    async def registration(self, user_model) -> JSONResponse:
        data = {"user_id": await self.orm.add_user(user_model)}
        access = await self.jwt_create(data).create_access()
        refresh = await self.jwt_create(data).create_refresh()
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
        user = await self.func(dictgetdatatoken)
        stmt = await stmt_get(user.get("email"))
        if stmt.email == user.get("email").lower():
            data = {"user_id": stmt.id}
            access = await self.jwt_create(data).create_access()
            refresh = await self.jwt_create(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

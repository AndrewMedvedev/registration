from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.interfaces import AuthorizationsBase
from src.services.orm import ORMService

from .controls import Send
from .jwt_classes import JWTCreate


class ReUse(AuthorizationsBase):

    def __init__(self):
        self.orm = ORMService()
        self.jwt_create = JWTCreate()
        self.send = Send()

    @staticmethod
    async def link(setting: str, dictlink: dict, code_verifier: str) -> JSONResponse:
        url = f"{setting}?{'&'.join([f'{k}={v}' for k, v in dictlink.items()])}"
        return JSONResponse(content={"url": url, "code_verifier": code_verifier})

    async def get_token(
        self,
        dictgetdata: dict,
        setting: str,
        service: str,
    ) -> JSONResponse:
        match service:
            case "vk":
                return JSONResponse(
                    content=await self.send.post_data(
                        params=dictgetdata,
                        setting=setting,
                    )
                )
            case "yandex":
                return JSONResponse(
                    content=await self.send.post_data_yandex(
                        params=dictgetdata,
                        setting=setting,
                    )
                )

    async def registration(self, user_model: BaseModel) -> JSONResponse:
        await self.orm.add_user(user_model)
        return JSONResponse(content={"message": 200})

    async def login(
        self,
        dictgetdatatoken: dict,
        setting: str,
        service: str,
    ) -> JSONResponse:
        match service:
            case "vk":
                user = (
                    await self.send.post_data(
                        params=dictgetdatatoken,
                        setting=setting,
                    )
                ).get("user")
                stmt = await self.orm.get_user_email_vk(user.get("email").lower())
                if stmt.email == user.get("email").lower():
                    return await self.jwt_create.create_tokens(stmt.user_id)
            case "yandex":
                user = await self.send.get_data(
                    params=dictgetdatatoken,
                    setting=setting,
                )
                stmt = await self.orm.get_user_email_yandex(
                    user.get("default_email").lower()
                )
                if stmt.email == user.get("default_email").lower():
                    return await self.jwt_create.create_tokens(stmt.user_id)

import logging

from fastapi import status
from pydantic import BaseModel

from src.interfaces import AuthorizationsBase
from src.services.orm import ORMService
from src.responses import CustomResponse
from .controls import Send
from .jwt_classes import JWTCreate

log = logging.getLogger(__name__)


class ReUse(AuthorizationsBase):

    def __init__(self):
        self.orm = ORMService()
        self.jwt_create = JWTCreate()
        self.send = Send()

    @staticmethod
    async def link(
        setting: str,
        dictlink: dict,
        code_verifier: str,
    ) -> CustomResponse:
        url = f"{setting}?{'&'.join([f'{k}={v}' for k, v in dictlink.items()])}"
        return CustomResponse(
            body={"url": url, "code_verifier": code_verifier},
            status_code=status.HTTP_200_OK,
        )

    async def get_token(
        self,
        dictgetdata: dict,
        setting: str,
        service: str,
    ) -> CustomResponse:
        match service:
            case "vk":
                return CustomResponse(
                    body=await self.send.post_data(
                        params=dictgetdata,
                        setting=setting,
                    ),
                    status_code=status.HTTP_200_OK,
                )
            case "yandex":
                return CustomResponse(
                    body=await self.send.post_data_yandex(
                        params=dictgetdata,
                        setting=setting,
                    ),
                    status_code=status.HTTP_200_OK,
                )

    async def registration(self, user_model: BaseModel) -> CustomResponse:
        await self.orm.add_user(user_model)
        return CustomResponse(
            body={"message": 200},
            status_code=status.HTTP_201_CREATED,
        )

    async def login(
        self,
        dictgetdatatoken: dict,
        setting: str,
        service: str,
    ) -> CustomResponse:
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
                    return CustomResponse(
                        body=await self.jwt_create.create_tokens(stmt.user_id),
                        status_code=status.HTTP_200_OK,
                    )
            case "yandex":
                user = await self.send.get_data(
                    params=dictgetdatatoken,
                    setting=setting,
                )
                stmt = await self.orm.get_user_email_yandex(
                    user.get("default_email").lower()
                )
                if stmt.email == user.get("default_email").lower():
                    return CustomResponse(
                        body=await self.jwt_create.create_tokens(stmt.user_id),
                        status_code=status.HTTP_200_OK,
                    )

from fastapi.responses import JSONResponse

from src.classes.reuse_class import ReUse
from src.config import Settings
from src.database import get_data_user_yandex, get_token_user_yandex
from src.database.models import UserYandex
from src.database.schemas import (
    DictGetDataTokenYandex,
    DictGetDataYandex,
    DictLinkYandex,
)
from src.services.orm import ORMService
from src.interfaces import OtherAuthorizationsBase


class Yandex(OtherAuthorizationsBase):

    def __init__(self, code: str = None, access_token: str = None) -> None:
        self.code = code
        self.access_token = access_token
        self.settings = Settings
        self.reuse = ReUse
        self.user = UserYandex

    async def link(
        self,
    ) -> str:
        return await self.reuse.link(
            setting=self.settings.YANDEX_AUTH_URL,
            dictlink=DictLinkYandex().model_dump(),
        )

    async def get_token(self) -> JSONResponse:
        return await self.reuse(
            func=get_token_user_yandex,
        ).get_token(
            dictgetdata=DictGetDataYandex(code=self.code).model_dump(),
        )

    async def registration(self) -> JSONResponse:
        user = await get_data_user_yandex(
            DictGetDataTokenYandex(oauth_token=self.access_token).model_dump()
        )
        user_model = self.user(
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            id_yandex=user.get("id"),
            login=user.get("login"),
            email=user.get("default_email"),
        )
        return await self.reuse().registration(
            user_model=user_model,
        )

    async def login(self) -> JSONResponse:
        return await self.reuse(
            func=get_data_user_yandex,
        ).login(
            dictgetdatatoken=DictGetDataTokenYandex(
                oauth_token=self.access_token
            ).model_dump(),
            stmt_get=ORMService().get_user_email_yandex,
        )

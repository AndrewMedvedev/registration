from fastapi.responses import JSONResponse

from src.config import Settings
from src.database.models import UserYandex
from src.database.schemas import (DictGetDataTokenYandex, DictGetDataYandex,
                                  DictLinkYandex, RegistrationYandex)
from src.interfaces import AuthorizationsBase
from src.responses import CustomResponse
from .controls import create_codes
from .reuse_class import ReUse


class Yandex(AuthorizationsBase):

    def __init__(self) -> None:
        self.settings = Settings
        self.reuse = ReUse()
        self.user = UserYandex

    async def link(
        self,
    ) -> CustomResponse:
        codes = await create_codes()
        return await self.reuse.link(
            setting=self.settings.YANDEX_AUTH_URL,
            dictlink=DictLinkYandex(
                code_challenge=codes.get("code_challenge")
            ).model_dump(),
            code_verifier=codes.get("code_verifier"),
        )

    async def get_token(
        self,
        code: str,
        code_verifier: str,
    ) -> CustomResponse:
        return await self.reuse.get_token(
            dictgetdata=DictGetDataYandex(
                code=code,
                code_verifier=code_verifier,
            ).model_dump(),
            setting=self.settings.YANDEX_TOKEN_URL,
            service="yandex",
        )

    async def registration(self, model: RegistrationYandex) -> CustomResponse:
        user_model = self.user(
            user_id=model.user_id,
            first_name=model.first_name,
            last_name=model.last_name,
            id_yandex=model.id_yandex,
            login=model.login,
            email=model.email,
        )
        return await self.reuse.registration(
            user_model=user_model,
        )

    async def login(self, access_token: str) -> CustomResponse:
        return await self.reuse.login(
            dictgetdatatoken=DictGetDataTokenYandex(
                oauth_token=access_token
            ).model_dump(),
            setting=self.settings.YANDEX_API_URL,
            service="yandex",
        )

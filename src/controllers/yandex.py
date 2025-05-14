from config import settings

from ..database.crud import SQLYandex
from ..jwt import JWTCreate
from ..rest import YandexApi
from ..schemas import (
    DictGetDataTokenYandex,
    DictGetDataYandex,
    DictLinkYandex,
    RegistrationYandex,
)
from ..utils import create_codes


class YandexControl:
    def __init__(self) -> None:
        self.sql_yandex = SQLYandex()
        self.jwt_create = JWTCreate()
        self.yandex_api = YandexApi()

    @staticmethod
    async def link() -> dict:
        codes = create_codes()
        dict_link = DictLinkYandex(code_challenge=codes["code_challenge"]).model_dump().items()
        url = f"{settings.YANDEX_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in dict_link])}"
        return {
            "link": url,
            "code_verifier": codes["code_verifier"],
        }

    async def get_token(
        self,
        code: str,
        code_verifier: str,
    ) -> dict:
        params = DictGetDataYandex(
            code=code,
            code_verifier=code_verifier,
        ).model_dump()
        return await self.yandex_api.get_token(params=params)

    async def registration(self, model: RegistrationYandex) -> None:
        return await self.sql_yandex.create_user(model=model.to_model())

    async def login(self, access_token: str) -> dict:
        params = DictGetDataTokenYandex(oauth_token=access_token).model_dump()
        user = await self.yandex_api.get_data(params=params)
        user_id = await self.sql_yandex.get_user_email(email=user["default_email"])
        return await self.jwt_create.create_tokens(user_id=user_id)

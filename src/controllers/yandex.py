from config import settings

from ..baseclasses import BaseControl
from ..database.crud import RedisOtherAuth, SQLYandex
from ..jwt import JWTCreate
from ..rest import YandexApi
from ..schemas import (
    DictGetDataTokenYandex,
    DictGetDataYandex,
    DictLinkYandex,
    RegistrationYandex,
)
from ..utils import create_codes


class YandexControl(BaseControl):
    def __init__(self) -> None:
        self.sql_yandex = SQLYandex()
        self.redis = RedisOtherAuth()
        self.jwt_create = JWTCreate()
        self.yandex_api = YandexApi()

    async def link(self) -> str:
        codes = create_codes()
        await self.redis.add_code(schema=codes)
        dict_link = (
            DictLinkYandex(state=codes.state, code_challenge=codes.code_challenge)
            .model_dump()
            .items()
        )
        url = f"{settings.YANDEX_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in dict_link])}"
        self.logger.warning(url)
        return url

    async def get_token(self, code: str, state: str) -> str:
        data_state = await self.redis.get_code(key=state)
        params = DictGetDataYandex(
            code=code,
            code_verifier=data_state,
        ).model_dump()
        result = await self.yandex_api.get_token(params=params)
        self.logger.warning(result)
        return result["access_token"]

    async def registration(self, model: RegistrationYandex) -> None:
        return await self.sql_yandex.create_user(model=model.to_model())

    async def login(self, code: str, state: str) -> dict:
        token = await self.get_token(code=code, state=state)
        self.logger.warning(token)
        params = DictGetDataTokenYandex(oauth_token=token).model_dump()
        user = await self.yandex_api.get_data(params=params)
        self.logger.warning(user)
        user_id = await self.sql_yandex.get_user_email(email=user["default_email"])
        return await self.jwt_create.create_tokens(user_id=user_id)

from config import settings

from ..database.crud import SQLVK, RedisOtherAuth
from ..jwt import JWTCreate
from ..rest import VKApi
from ..schemas import (
    DictGetDataTokenVK,
    DictGetDataVK,
    DictLinkVK,
    RegistrationVKSchema,
)
from ..utils import create_codes


class VKControl:
    def __init__(self) -> None:
        self.sql_vk = SQLVK()
        self.redis = RedisOtherAuth()
        self.jwt_create = JWTCreate()
        self.vk_api = VKApi()

    async def link(self) -> str:
        codes = create_codes()
        await self.redis.add_code(schema=codes)
        dict_link = (
            DictLinkVK(state=codes.state, code_challenge=codes.code_challenge).model_dump().items()
        )
        return f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in dict_link])}"

    async def get_token(self, code: str, device_id: str, state: str) -> str:
        data_state = await self.redis.get_code(key=state)
        params = DictGetDataVK(
            code=code, device_id=device_id, code_verifier=data_state, state=state
        ).model_dump()
        result = await self.vk_api.get_token(params=params)
        return result["access_token"]

    async def registration(self, model: RegistrationVKSchema) -> None:
        return await self.sql_vk.create_user(model=model.to_model())

    async def login(self, code: str, device_id: str, state: str) -> dict:
        token = await self.get_token(code=code, device_id=device_id, state=state)
        params = DictGetDataTokenVK(access_token=token).model_dump()
        user = await self.vk_api.get_data(params=params)
        user_id = await self.sql_vk.get_user_email(email=user["email"].lower())
        return await self.jwt_create.create_tokens(user_id=user_id)

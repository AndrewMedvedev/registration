from config import settings

from ..database.crud import SQLVK
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
    def __init__(self):
        self.sql_vk = SQLVK()
        self.jwt_create = JWTCreate()
        self.vk_api = VKApi()

    @staticmethod
    async def link() -> dict:
        codes = create_codes()
        dict_link = DictLinkVK(code_challenge=codes["code_challenge"]).model_dump().items()
        url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in dict_link])}"
        return {
            "link": url,
            "code_verifier": codes["code_verifier"],
        }

    async def get_token(self, code: str, device_id: str, code_verifier: str) -> dict:
        params = DictGetDataVK(
            code=code,
            device_id=device_id,
            code_verifier=code_verifier,
        ).model_dump()
        return await self.vk_api.get_token(params=params)

    async def registration(self, model: RegistrationVKSchema) -> None:
        return await self.sql_vk.create_user(model=model.to_model())

    async def login(self, access_token: str) -> dict:
        params = DictGetDataTokenVK(access_token=access_token).model_dump()
        user = await self.vk_api.get_data(params=params)
        user_id = await self.sql_vk.get_user_email(email=user["email"].lower())
        return await self.jwt_create.create_tokens(user_id=user_id)

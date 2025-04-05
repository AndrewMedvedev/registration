
from src.config import Settings
from src.database.models import UserVk
from src.database.schemas import DictGetDataTokenVK, DictGetDataVK, DictLinkVK, RegistrationVK
from src.interfaces import AuthorizationsBase
from src.responses import CustomResponse

from .controls import create_codes
from .reuse_class import ReUse


class VK(AuthorizationsBase):

    def __init__(self) -> None:
        self.settings = Settings
        self.reuse = ReUse()
        self.user = UserVk

    async def link(
        self,
    ) -> CustomResponse:
        codes = await create_codes()
        return await self.reuse.link(
            setting=self.settings.VK_AUTH_URL,
            dictlink=DictLinkVK(
                code_challenge=codes.get("code_challenge")
            ).model_dump(),
            code_verifier=codes.get("code_verifier"),
        )

    async def get_token(
        self,
        code: str,
        device_id: str,
        code_verifier: str,
    ) -> CustomResponse:
        return await self.reuse.get_token(
            dictgetdata=DictGetDataVK(
                code=code,
                device_id=device_id,
                code_verifier=code_verifier,
            ).model_dump(),
            setting=self.settings.VK_TOKEN_URL,
            service="vk",
        )

    async def registration(self, model: RegistrationVK) -> CustomResponse:
        user_model = self.user(
            user_id=model.user_id,
            first_name=model.first_name,
            last_name=model.last_name,
            id_vk=model.id_vk,
            email=model.email.lower(),
        )
        return await self.reuse.registration(
            user_model=user_model,
        )

    async def login(self, access_token: str) -> CustomResponse:
        return await self.reuse.login(
            dictgetdatatoken=DictGetDataTokenVK(access_token=access_token).model_dump(),
            setting=self.settings.VK_API_URL,
            service="vk",
        )

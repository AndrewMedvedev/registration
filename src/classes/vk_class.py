from fastapi.responses import JSONResponse

from src.classes.reuse_class import ReUse
from src.config import Settings as settings
from src.database import get_data_user_vk, get_token_user_vk
from src.database.models import UserVk
from src.database.schemas import DictGetDataTokenVK, DictGetDataVK, DictLinkVK
from src.services.orm import ORMService


class VK:

    def __init__(
        self,
        code: str = None,
        device_id: str = None,
        access_token: str = None,
    ) -> None:
        self.code = code
        self.device_id = device_id
        self.access_token = access_token

    @staticmethod
    async def vk_link() -> str:
        return await ReUse.link(
            setting=settings.VK_AUTH_URL,
            dictlink=DictLinkVK().model_dump(),
        )

    async def vk_get_token(self) -> JSONResponse:
        return await ReUse(
            func=get_token_user_vk,
        ).get_token(
            dictgetdata=DictGetDataVK(
                code=self.code, device_id=self.device_id
            ).model_dump(),
        )

    async def vk_registration(self) -> JSONResponse:
        user = await get_data_user_vk(
            DictGetDataTokenVK(access_token=self.access_token).model_dump()
        )
        user_model = UserVk(
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            id_vk=int(user.get("user_id")),
            email=user.get("email").lower(),
        )
        return await ReUse.registration(
            user_model=user_model,
        )

    async def vk_login(self) -> JSONResponse:
        return await ReUse(
            func=get_data_user_vk,
        ).login(
            dictgetdatatoken=DictGetDataTokenVK(
                access_token=self.access_token
            ).model_dump(),
            stmt_get=ORMService().get_user_email_vk,
        )

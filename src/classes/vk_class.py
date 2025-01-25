from src.database.models import UserVk
from src.classes.jwt_classes import JWTCreate
from src.services.orm import ORMService
from src.config import Settings as settings
from src.database.schemas.vk_schemas import DictLinkVK, DictGetDataVK
from src.database.controls import get_data_user_vk


class VK:

    def __init__(self, code: str = None) -> None:
        self.code = code

    async def vk_link() -> str:
        url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in DictLinkVK().model_dump().items()])}"
        return url

    async def vk_registration(self) -> dict:
        model = DictGetDataVK(code=self.code).model_dump()
        user = await get_data_user_vk(model)
        user_model = UserVk(
            id_vk=user.get("user_id"),
            email=user.get("email"),
        )
        await ORMService().add_user(user_model)
        data = {"user_name": user.get("email")}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return {
            "access": access,
            "refresh": refresh,
        }

    async def vk_login(self) -> dict:
        model = DictGetDataVK(code=self.code).model_dump()
        user = await get_data_user_vk(model)
        stmt = await ORMService().get_user_email_vk(user.get("email"))
        print(user.get("email"))
        if stmt.email == user.get("email"):
            data = {"user_name": user.get("email")}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return {
                "access": access,
                "refresh": refresh,
            }

from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.config import Settings as settings
from src.database import UserVk, get_data_user_vk, get_token_user_vk
from src.database.schemas import DictGetDataTokenVK, DictGetDataVK, DictLinkVK
from src.services.orm import ORMService


class VK:

    def __init__(
        self, code: str = None, device_id: str = None, access_token: str = None
    ) -> None:
        self.code = code
        self.device_id = device_id
        self.access_token = access_token

    async def vk_link() -> str:
        url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in DictLinkVK().model_dump().items()])}"
        return url

    async def vk_get_token(self) -> str:
        model = DictGetDataVK(code=self.code, device_id=self.device_id).model_dump()
        user = await get_token_user_vk(model)
        return user

    async def vk_registration(self) -> JSONResponse:
        model = DictGetDataTokenVK(access_token=self.access_token).model_dump()
        user = await get_data_user_vk(model)
        user_model = UserVk(
            id_vk=int(user.get("user_id")),
            email=user.get("email").lower(),
        )
        await ORMService().add_user(user_model)
        data = {"user_name": user.get("email")}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

    async def vk_login(self) -> JSONResponse:
        model = DictGetDataTokenVK(access_token=self.access_token).model_dump()
        user = await get_data_user_vk(model)
        stmt = await ORMService().get_user_email_vk(user.get("email").lower())
        if stmt.email == user.get("email").lower():
            data = {"user_name": user.get("email").lower()}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

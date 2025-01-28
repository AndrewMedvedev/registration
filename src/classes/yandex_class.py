from src.database.schemas.yandex_schemas import (
    DictLinkYandex,
    DictGetDataYandex,
    DictGetDataTokenYandex,
)
from src.database.controls import (
    get_token_user_yandex,
    get_data_user_yandex,
)
from src.config import Settings as settings
from src.database.models import UserYandex
from src.services.orm import ORMService
from src.classes.jwt_classes import JWTCreate


class Yandex:

    def __init__(self, code: str = None, access_token: str = None) -> None:
        self.code = code
        self.access_token = access_token

    async def yandex_link() -> str:
        url = f"{settings.YANDEX_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in DictLinkYandex().model_dump().items()])}"
        return url

    async def yandex_get_token(self) -> str:
        model = DictGetDataYandex(code=self.code).model_dump()
        user = await get_token_user_yandex(model)
        return user

    async def yandex_registration(self) -> dict:
        model = DictGetDataTokenYandex(oauth_token=self.access_token).model_dump()
        user = await get_data_user_yandex(model)
        user_model = UserYandex(
            id_yandex=user.get("id"),
            login=user.get("login"),
            email=user.get("default_email"),
        )
        await ORMService().add_user(user_model)
        data = {"user_name": user.get("default_email")}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return {
            "access": access,
            "refresh": refresh,
        }

    async def yandex_login(self) -> dict:
        model = DictGetDataTokenYandex(oauth_token=self.access_token).model_dump()
        user = await get_data_user_yandex(model)
        stmt = await ORMService().get_user_email_yandex(user.get("default_email"))
        if stmt.email == user.get("default_email"):
            data = {"user_name": user.get("default_email")}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return {
                "access": access,
                "refresh": refresh,
            }
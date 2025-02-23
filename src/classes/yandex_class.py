from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.config import Settings as settings
from src.database import get_data_user_yandex, get_token_user_yandex
from src.database.models import UserYandex
from src.database.schemas import (DictGetDataTokenYandex, DictGetDataYandex,
                                  DictLinkYandex)
from src.services.orm import ORMService


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

    async def yandex_registration(self) -> JSONResponse:
        model = DictGetDataTokenYandex(oauth_token=self.access_token).model_dump()
        user = await get_data_user_yandex(model)
        print(user)
        user_model = UserYandex(
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            id_yandex=user.get("id"),
            login=user.get("login"),
            email=user.get("default_email"),
        )
        user_id = await ORMService().add_user(user_model)
        data = {"user_id": user_id}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

    async def yandex_login(self) -> JSONResponse:
        model = DictGetDataTokenYandex(oauth_token=self.access_token).model_dump()
        user = await get_data_user_yandex(model)
        print(user)
        stmt = await ORMService().get_user_email_yandex(user.get("default_email"))
        if stmt.email == user.get("default_email"):
            data = {"user_id": stmt.id}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

from src.database.schemas.mail_ru_schemas import (
    DictLinkMailRu,
    DictGetDataMailRu,
    DictGetDataTokenMailRu,
)
from src.database.controls import (
    get_data_user_mail_ru,
    get_token_user_mail_ru,
)
from src.config import Settings as settings
from src.database.models import UserMailRu
from src.services.orm import ORMService
from src.classes.jwt_classes import JWTCreate


class MailRu:

    def __init__(self, code: str = None, access_token: str = None) -> None:
        self.code = code
        self.access_token = access_token

    async def mail_ru_link() -> str:
        url = f"{settings.MAIL_RU_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in DictLinkMailRu().model_dump().items()])}"
        return url

    async def mail_ru_get_token(self) -> str:
        model = DictGetDataMailRu(code=self.code).model_dump()
        user = await get_token_user_mail_ru(params=model)
        return user

    async def mail_ru_registration(self) -> dict:
        model = DictGetDataTokenMailRu(access_token=self.access_token).model_dump()
        user = await get_data_user_mail_ru(model)
        user_model = UserMailRu(
            id_mail_ru=user.get("id"),
            email=user.get("email"),
            birthday=user.get("birthday"),
        )
        await ORMService().add_user(user_model)
        data = {"user_name": user.get("email")}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return {
            "access": access,
            "refresh": refresh,
        }

    async def mail_ru_login(self) -> dict:
        model = DictGetDataTokenMailRu(access_token=self.access_token).model_dump()
        user = await get_data_user_mail_ru(model)
        stmt = await ORMService().get_user_email_mail_ru(user.get("email"))
        if stmt.email == user.get("email"):
            data = {"user_name": user.get("email")}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return {
                "access": access,
                "refresh": refresh,
            }

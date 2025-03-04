from fastapi.responses import JSONResponse

from src.classes.reuse_class import ReUse
from src.config import Settings
from src.database import get_data_user_mail_ru, get_token_user_mail_ru
from src.database.models import UserMailRu
from src.database.schemas import (DictGetDataMailRu, DictGetDataTokenMailRu,
                                  DictLinkMailRu)
from src.interfaces import OtherAuthorizationsBase
from src.services.orm import ORMService


class MailRu(OtherAuthorizationsBase):

    def __init__(
        self,
        code: str = None,
        access_token: str = None,
    ) -> None:
        self.code = code
        self.access_token = access_token
        self.settings = Settings
        self.reuse = ReUse
        self.user = UserMailRu

    async def link(
        self,
    ) -> str:
        return await self.reuse.link(
            setting=self.settings.MAIL_RU_AUTH_URL,
            dictlink=DictLinkMailRu().model_dump(),
        )

    async def get_token(self) -> JSONResponse:
        return await self.reuse(
            func=get_token_user_mail_ru,
        ).get_token(
            dictgetdata=DictGetDataMailRu(code=self.code).model_dump(),
        )

    async def registration(self) -> JSONResponse:
        user = await get_data_user_mail_ru(
            DictGetDataTokenMailRu(access_token=self.access_token).model_dump()
        )
        user_model = self.user(
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            id_mail_ru=user.get("id"),
            email=user.get("email"),
            birthday=user.get("birthday"),
        )
        return await self.reuse().registration(user_model=user_model)

    async def login(self) -> JSONResponse:
        return await self.reuse(
            func=get_data_user_mail_ru,
        ).login(
            dictgetdatatoken=DictGetDataTokenMailRu(
                access_token=self.access_token
            ).model_dump(),
            stmt_get=ORMService().get_user_email_mail_ru,
        )

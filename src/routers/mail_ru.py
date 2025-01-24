from fastapi import APIRouter, HTTPException
from src.classes.mail_ru_class import MailRu

router = APIRouter(prefix="/mail.ru", tags=["mail.ru"])


@router.get(
    "/link",
    response_model=None,
)
async def mail_ru_link() -> str:
    return await MailRu.mail_ru_link()


@router.get(
    "/get/token",
    response_model=None,
)
async def mail_ru_get_token(code: str) -> str:
    return await MailRu(code=code).mail_ru_get_token()


@router.get(
    "/registration",
    response_model=None,
)
async def mail_ru_registration(access_token: str) -> dict:
    return await MailRu(access_token=access_token).mail_ru_registration()


@router.get(
    "/login",
    response_model=None,
)
async def mail_ru_login(access_token: str) -> dict | HTTPException:
    return await MailRu(access_token=access_token).mail_ru_login()

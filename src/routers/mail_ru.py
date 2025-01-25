from fastapi import APIRouter, HTTPException, status
from src.classes.mail_ru_class import MailRu

router = APIRouter(prefix="/mail.ru", tags=["mail.ru"])


@router.get(
    "/link",
    response_model=None,
)
async def mail_ru_link() -> str | HTTPException:
    try:
        return await MailRu.mail_ru_link()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/get/token",
    response_model=None,
)
async def mail_ru_get_token(code: str) -> str | HTTPException:
    try:
        return await MailRu(code=code).mail_ru_get_token()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/registration",
    response_model=None,
)
async def mail_ru_registration(access_token: str) -> dict | HTTPException:
    try:
        return await MailRu(access_token=access_token).mail_ru_registration()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/login",
    response_model=None,
)
async def mail_ru_login(access_token: str) -> dict | HTTPException:
    try:
        return await MailRu(access_token=access_token).mail_ru_login()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

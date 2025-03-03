from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.classes.mail_ru_class import MailRu

router_mail_ru = APIRouter(prefix="/api/v1/mail.ru", tags=["mail.ru"])


@router_mail_ru.get(
    "/link",
    response_model=None,
)
async def mail_ru_link() -> str | JSONResponse:
    try:
        return await MailRu().mail_ru_link()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_mail_ru.get(
    "/get/token/{code}",
    response_model=None,
)
async def mail_ru_get_token(code: str) -> JSONResponse:
    try:
        return await MailRu(code=code).mail_ru_get_token()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_mail_ru.post(
    "/registration/{access_token}",
    response_model=None,
)
async def mail_ru_registration(access_token: str) -> JSONResponse:
    try:
        return await MailRu(access_token=access_token).mail_ru_registration()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_mail_ru.post(
    "/login/{access_token}",
    response_model=None,
)
async def mail_ru_login(access_token: str) -> JSONResponse:
    try:
        return await MailRu(access_token=access_token).mail_ru_login()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

from fastapi import Request, status
from fastapi.responses import JSONResponse

from .errors import (
    DataBaseError,
    JWTCreateError,
    PasswordError,
    SendError,
    EmailError,
    PhoneNumberError,
)
from src.responses import CustomBadResponse


async def db_error(
    request: Request,
    exc: DataBaseError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        detail="Ошибка базы данных",
    )


async def password_error(
    request: Request,
    exc: PasswordError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        detail="Ошибка пароля",
    )


async def jwt_error(
    request: Request,
    exc: JWTCreateError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        detail="Ошибка создания токенов",
    )


async def send_error(
    request: Request,
    exc: SendError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
        detail="Ошибка отправки",
    )


async def email_error(
    request: Request,
    exc: EmailError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        detail="Ошибка email",
    )


async def phone_number_error(
    request: Request,
    exc: PhoneNumberError,
) -> CustomBadResponse:
    return CustomBadResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        message=str(exc),
        detail="Ошибка phone number",
    )

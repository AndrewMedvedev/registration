from fastapi import Request, status
from fastapi.responses import JSONResponse

from .errors import DataBaseError, JWTCreateError, PasswordError, SendError


async def db_error(
    request: Request,
    exc: DataBaseError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )



async def password_error(
    request: Request,
    exc: PasswordError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


async def jwt_error(
    request: Request,
    exc: JWTCreateError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


async def send_error(
    request: Request,
    exc: SendError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )
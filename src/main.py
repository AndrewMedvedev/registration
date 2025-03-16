import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.classes.controls import config_logging
from src.errors import DataBaseError, JWTCreateError, PasswordError, SendError
from src.routers import (router_authorization, router_data,
                         router_validate_jwt, router_vk, router_yandex)

limiter = Limiter(key_func=get_remote_address, default_limits=["10/second"])

config_logging(level=logging.INFO)

app = FastAPI(title="Регистрация")

app.include_router(router_authorization)

app.include_router(router_vk)

app.include_router(router_yandex)

app.include_router(router_validate_jwt)

app.include_router(router_data)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(DataBaseError)
async def db_error(
    request: Request,
    exc: DataBaseError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


@app.exception_handler(PasswordError)
async def password_error(
    request: Request,
    exc: PasswordError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


@app.exception_handler(JWTCreateError)
async def jwt_error(
    request: Request,
    exc: JWTCreateError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )


@app.exception_handler(SendError)
async def send_error(
    request: Request,
    exc: SendError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )


app.add_middleware(SlowAPIMiddleware)

origins = [
    "http://localhost:3000",
    "https://register-666-ramzer.onrender.com",
    "https://frontend-project-production-6352.up.railway.app",
    "https://admin-panel-production-19ca.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

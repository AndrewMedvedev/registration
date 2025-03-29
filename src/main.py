import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.classes.controls import config_logging
from src.errors import (
    DataBaseError,
    JWTCreateError,
    PasswordError,
    SendError,
    EmailError,
    PhoneNumberError,
    db_error,
    jwt_error,
    password_error,
    send_error,
    email_error,
    phone_number_error,
)
from src.routers import (
    router_authorization,
    router_data,
    router_validate_jwt,
    router_vk,
    router_yandex,
)

limiter = Limiter(key_func=get_remote_address, default_limits=["10/second"])

config_logging(level=logging.INFO)

app = FastAPI(title="Регистрация")

origins = [
    "http://localhost:3000",
    "https://register-666-ramzer.onrender.com",
    "https://frontend-project-production-6352.up.railway.app",
    "https://admin-panel-production-19ca.up.railway.app",
    "https://online-service-for-applicants.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_exception_handler(DataBaseError, db_error)

app.add_exception_handler(PasswordError, password_error)

app.add_exception_handler(JWTCreateError, jwt_error)

app.add_exception_handler(SendError, send_error)

app.add_exception_handler(EmailError, email_error)

app.add_exception_handler(PhoneNumberError, phone_number_error)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(SlowAPIMiddleware)

app.include_router(router_authorization)

app.include_router(router_vk)

app.include_router(router_yandex)

app.include_router(router_validate_jwt)

app.include_router(router_data)

app.state.limiter = limiter

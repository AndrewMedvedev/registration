import typing as t

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.exeptions import (
    BadRequestHTTPError,
    BaseHTTPError,
    HTTPException,
    InternalHTTPError,
    JSONError,
)
from src.routers import authorization, data, validate_jwt, vk, yandex

app = FastAPI(title="Registration service")


@app.exception_handler(Exception)
def handler(
    _request: Request,
    exception: t.Union[
        Exception,
        BaseException,
    ],
    description: t.Optional[str] = None,
) -> JSONResponse:
    if isinstance(exception, HTTPException):
        exception = BaseHTTPError(str(exception), exception.status_code)
    if isinstance(exception, BaseHTTPError):
        pass
    elif isinstance(exception, (AttributeError, ValueError, KeyError, TypeError)):
        description = description if description is not None else str(exception)
        exception = BadRequestHTTPError()

    else:
        exception = InternalHTTPError()

    return JSONResponse(
        content=JSONError.create(exception, description).to_dict(),
        status_code=exception.code,
    )


origins: list[str] = [
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


def include_routers(app: FastAPI):
    app.include_router(authorization)
    app.include_router(vk)
    app.include_router(yandex)
    app.include_router(data)
    app.include_router(validate_jwt)


include_routers(app)

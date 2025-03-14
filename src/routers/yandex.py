from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.classes.yandex_class import Yandex
from src.database.schemas import RegistrationYandex

router_yandex = APIRouter(prefix="/api/v1/yandex", tags=["yandex"])


@router_yandex.get(
    "/link",
    response_model=None,
)
async def yandex_link() -> JSONResponse:
    return await Yandex().link()


@router_yandex.get(
    "/get/token/{code}/{code_verifier}",
    response_model=None,
)
async def yandex_get_token(code: str, code_verifier: str) -> JSONResponse:
    return await Yandex().get_token(
        code=code,
        code_verifier=code_verifier,
    )


@router_yandex.post(
    "/registration/",
    response_model=RegistrationYandex,
)
async def yandex_registration(model: RegistrationYandex) -> JSONResponse:
    return await Yandex().registration(model=model)


@router_yandex.post(
    "/login/{access_token}",
    response_model=None,
)
async def yandex_login(access_token: str) -> JSONResponse:
    return await Yandex().login(access_token=access_token)

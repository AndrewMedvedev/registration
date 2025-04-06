from fastapi import APIRouter

from src.classes.yandex_class import Yandex
from src.database.schemas import RegistrationYandex
from src.responses import CustomResponse

router_yandex = APIRouter(prefix="/api/v1/yandex", tags=["yandex"])


@router_yandex.get(
    "/link",
    response_model=None,
)
async def yandex_link() -> CustomResponse:
    return await Yandex().link()


@router_yandex.get(
    "/get/token/{code}/{code_verifier}",
    response_model=None,
)
async def yandex_get_token(code: str, code_verifier: str) -> CustomResponse:
    return await Yandex().get_token(
        code=code,
        code_verifier=code_verifier,
    )


@router_yandex.post(
    "/registration/",
)
async def yandex_registration(model: RegistrationYandex) -> CustomResponse:
    return await Yandex().registration(model=model)


@router_yandex.post(
    "/login/{access_token}",
    response_model=None,
)
async def yandex_login(access_token: str) -> CustomResponse:
    return await Yandex().login(access_token=access_token)

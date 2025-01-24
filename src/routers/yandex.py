from fastapi import APIRouter, HTTPException
from src.classes.yandex_class import Yandex

router = APIRouter(prefix="/yandex", tags=["yandex"])


@router.get(
    "/link",
    response_model=None,
)
async def yandex_link() -> str:
    return await Yandex.yandex_link()


@router.get(
    "/get/token",
    response_model=None,
)
async def yandex_get_token(code: str) -> str:
    return await Yandex(code=code).yandex_get_token()


@router.get(
    "/registration",
    response_model=None,
)
async def yandex_registration(access_token: str) -> dict:
    return await Yandex(access_token=access_token).yandex_registration()


@router.get(
    "/login",
    response_model=None,
)
async def yandex_login(access_token: str) -> dict | HTTPException:
    return await Yandex(access_token=access_token).yandex_login()

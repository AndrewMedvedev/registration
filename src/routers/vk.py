from fastapi import APIRouter, HTTPException, status
from src.classes.vk_class import VK

router = APIRouter(prefix="/vk", tags=["vk"])


@router.get(
    "/link",
    response_model=None,
)
async def vk_link() -> str | HTTPException:
    try:
        return await VK.vk_link()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get(
    "/registration",
    response_model=None,
)
async def vk_registration(code: str) -> dict | HTTPException:
    try:
        return await VK(code=code).vk_registration()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get(
    "/login",
    response_model=None,
)
async def vk_login(code: str) -> dict | HTTPException:
    try:
        return await VK(code=code).vk_login()
    except:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/get/token",
    response_model=None,
)
async def vk_get_token(
    code: str,
    device_id: str,
) -> str | HTTPException:
    try:
        return await VK(
            code=code,
            device_id=device_id,
        ).vk_get_token()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/registration",
    response_model=None,
)
async def vk_registration(access_token: str) -> dict | HTTPException:
    try:
        return await VK(access_token=access_token).vk_registration()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/login",
    response_model=None,
)
async def vk_login(access_token: str) -> dict | HTTPException:
    try:
        return await VK(access_token=access_token).vk_login()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

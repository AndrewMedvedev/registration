from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.classes.vk_class import VK

router_vk = APIRouter(prefix="/vk", tags=["vk"])


@router_vk.get(
    "/link",
    response_model=None,
)
async def vk_link() -> str | HTTPException:
    try:
        return await VK.vk_link()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.get(
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
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.get(
    "/registration",
    response_model=None,
)
async def vk_registration(access_token: str) -> dict | HTTPException:
    try:
        return await VK(access_token=access_token).vk_registration()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.get(
    "/login",
    response_model=None,
)
async def vk_login(access_token: str) -> dict | HTTPException:
    try:
        return await VK(access_token=access_token).vk_login()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.classes.vk_class import VK
from src.database.schemas import RegistrationVK

router_vk = APIRouter(prefix="/api/v1/vk", tags=["vk"])


@router_vk.get(
    "/link",
    response_model=None,
)
async def vk_link() -> dict | JSONResponse:
    try:
        return await VK().link()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.get(
    "/get/token/{code}/{device_id}/{code_verifier}",
    response_model=None,
)
async def vk_get_token(
    code: str,
    device_id: str,
    code_verifier: str,
) -> JSONResponse:
    try:
        return await VK(
            code=code,
            device_id=device_id,
        ).get_token(code_verifier=code_verifier)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.post(
    "/registration/",
    response_model=RegistrationVK,
)
async def vk_registration(model: RegistrationVK) -> JSONResponse:
    try:
        return await VK().registration(model=model)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_vk.post(
    "/login/{access_token}",
    response_model=None,
)
async def vk_login(access_token: str) -> JSONResponse:
    try:
        return await VK(access_token=access_token).login()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

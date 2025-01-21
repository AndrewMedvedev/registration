from fastapi import APIRouter, HTTPException
from src.classes.vk_class import VK

router = APIRouter(prefix="/vk", tags=["vk"])


@router.get(
    "/link",
    response_model=None,
)
async def vk_link() -> str:
    return await VK().vk_link()



@router.get(
    "/registration",
    response_model=None,
)
async def vk_registration(code: str) -> dict:
    return await VK(code=code).vk_registration()


@router.get(
    "/login",
    response_model=None,
)
async def vk_login(code: str) -> dict | HTTPException:
    return await VK(code=code).vk_login()

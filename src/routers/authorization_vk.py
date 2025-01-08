from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from src.config import Settings as settings
import aiohttp

router = APIRouter(prefix="/authorization_vk", tags=["authorization_vk"])


@router.get("/login")
async def vk_login():
    params = {
        "client_id": settings.VK_CLIENT_ID,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "response_type": "code",
        "scope": "email",
        "display": "page",
    }
    url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return RedirectResponse(url)


@router.get("/callback")
async def vk_callback(code: str):
    """
    Эндпоинт для обработки ответа от VK.
    """
    params = {
        "client_id": settings.VK_CLIENT_ID,
        "client_secret": settings.VK_CLIENT_SECRET,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.VK_TOKEN_URL, params=params) as response:
            token_data = await response.json()
            if "error" in token_data:
                raise HTTPException(
                    status_code=400, detail=token_data["error_description"]
                )

            access_token = token_data["access_token"]
            user_id = token_data["user_id"]
            email = token_data.get("email")

            user_params = {
                "user_ids": user_id,
                "fields": "first_name,last_name",
                "access_token": access_token,
                "v": "5.131",
            }
            async with session.get(settings.VK_API_URL, params=user_params) as user_response:
                user_data = await user_response.json()
                if "error" in user_data:
                    raise HTTPException(
                        status_code=400, detail=user_data["error"]["error_msg"]
                    )

                user_info = user_data["response"][0]

                return {
                    "user_id": user_id,
                    "email": email,
                    "first_name": user_info["first_name"],
                    "last_name": user_info["last_name"],
                }

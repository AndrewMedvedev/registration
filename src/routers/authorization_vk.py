import base64
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from src.config import Settings as settings
import aiohttp

router = APIRouter(prefix="/authorization_vk", tags=["authorization_vk"])


@router.get("/login")
async def vk_login():
    # params = {
    #     "response_type": "code",
    #     "client_id": settings.VK_APP_ID,
    #     "code_verifier": settings.CODE_VERIFIER,
    #     "code_challenge_method": "S256",
    #     "code_challenge": base64.encode("S256"(settings.CODE_VERIFIER)),
    #     "redirect_uri": settings.VK_REDIRECT_URI,
    #     "state": settings.STATE,
    #     "scope": "email",
    # }

    params = {
        "response_type": "code",
        "client_id": settings.VK_APP_ID,
        "scope": "email phone",
        "redirect_uri": settings.VK_REDIRECT_URI,
        "state": settings.STATE,
        "code_challenge": settings.CODE_CHALLENGE,
    }
    url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    print(url)
    return url


# @router.get("/callback")
# async def vk_callback(code: str):
#     """
#     Эндпоинт для обработки ответа от VK.
#     """
#     params = {
#         "client_secret": settings.CLIENT_SECRET,
#         "grant_type": "authorization_code",
#         "code_verifier": settings.CODE_VERIFIER,
#         "redirect_uri": settings.VK_REDIRECT_URI,
#         "code": code,
#         "client_id": settings.VK_APP_ID,
#         "state": settings.STATE,
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.get(settings.VK_TOKEN_URL, params=params) as ses:
#             token_data = await ses.json()
#             if "error" in token_data:
#                 raise HTTPException(
#                     status_code=400, detail=token_data["error_description"]
#                 )

#             access_token = token_data["access_token"]
#             user_id = token_data["user_id"]
#             email = token_data.get("email")

#             user_params = {
#                 "user_ids": user_id,
#                 "fields": "first_name,last_name",
#                 "access_token": access_token,
#                 "v": "5.131",
#             }
#             async with session.get(
#                 settings.VK_API_URL, params=user_params
#             ) as user_response:
#                 user_data = await user_response.json()
#                 if "error" in user_data:
#                     raise HTTPException(
#                         status_code=400, detail=user_data["error"]["error_msg"]
#                     )

#                 user_info = user_data["response"][0]

#                 return {
#                     "user_id": user_id,
#                     "email": email,
#                     "first_name": user_info["first_name"],
#                     "last_name": user_info["last_name"],
#                 }


@router.get("/callback")
async def vk_callback(code: str):
    """
    Эндпоинт для обработки ответа от VK.
    """
    params = {
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code_verifier": settings.CODE_VERIFIER,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
        "client_id": settings.VK_APP_ID,
        "state": settings.STATE,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.VK_TOKEN_URL, params=params,ssl=False) as ses:
            token_data = await ses.json()
            if "error" in token_data:
                raise HTTPException(
                    status_code=400, detail=token_data["error_description"]
                )
            return token_data
        


@router.get("/user_data_vk")
async def user_data_vk(token: str):
    params = {
        "access_token": token,
        "client_id": settings.VK_APP_ID,
        'v': '5.199',
        'fields': 'id,first_name,last_name,sex'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
                    settings.VK_API_URL, params=params,ssl=False) as user_response:
                    user_data = await user_response.json()
                    return user_data
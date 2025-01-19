from fastapi import APIRouter, HTTPException, status
from src.config import Settings as settings
from src.database.models import UserVk
from src.database.schemas import VKModel
from src.classes.vk_class import VK

router = APIRouter(prefix="/vk", tags=["vk"])


@router.get("/link")
async def vk_link() -> str:
    params = {
        "response_type": "code",
        "client_id": settings.VK_APP_ID,
        "scope": "email",
        "redirect_uri": settings.VK_REDIRECT_URI,
        "state": settings.STATE,
        "code_challenge": settings.CODE_CHALLENGE,
    }
    url = f"{settings.VK_AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return url


@router.get(
    "/registration",
    response_model=None,
)
async def vk_registration(code: str) -> dict:
    params = {
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code_verifier": settings.CODE_VERIFIER,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
        "client_id": settings.VK_APP_ID,
        "state": settings.STATE,
    }
    user = await VK(params).get_data_user()
    user_model = UserVk(id_vk=user.get("user_id"), email=user.get("email"))
    await VK(user_model=user_model).data_add()
    data = {"user_name": user.get("email")}
    tokens = await VK(data=data).create_tokens()
    return {"access": tokens.get("access"), "refresh": tokens.get("refresh")}


@router.get(
    "/login",
    response_model=None,
)
async def vk_login(code: str) -> dict | HTTPException:
    params = {
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code_verifier": settings.CODE_VERIFIER,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
        "client_id": settings.VK_APP_ID,
        "state": settings.STATE,
    }
    user = await VK(params).get_data_user()
    stmt = await VK(email=user.get("email")).data_get()
    if stmt is not False:
        data = {"user_name": user.get("email")}
        tokens = await VK(data=data).create_tokens()
        return {"access": tokens.get("access"), "refresh": tokens.get("refresh")}
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

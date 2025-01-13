from fastapi import APIRouter, Request, HTTPException, Response, status
from src.services.orm import ORMService
from src.config import Settings as settings
from src.database.models import UserVk
from src.database.controls import VKControls
from src.database.controls import JWTControl

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


@router.get("/registration")
async def vk_registration(response: Response, code: str):
    params = {
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code_verifier": settings.CODE_VERIFIER,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
        "client_id": settings.VK_APP_ID,
        "state": settings.STATE,
    }
    user = await VKControls.get_token(params)
    token_control = JWTControl()
    user_model = UserVk(
        id_vk=user.get("user_id"),
        email=(user.get("email")).lower()
    )
    await ORMService().add_user(user_model)
    data_tkn = {"user_name": user.get("user_id")}
    access = await token_control.create_access(data_tkn)
    refresh = await token_control.create_refresh(data_tkn)
    response.set_cookie(
    key="access", value=access, httponly=True, secure=True, samesite="none"
)
    return {"refresh": refresh}

        # return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        


@router.get("/login")
async def vk_login(response: Response, code: str):
    params = {
        "client_secret": settings.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code_verifier": settings.CODE_VERIFIER,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
        "client_id": settings.VK_APP_ID,
        "state": settings.STATE,
    }
    user = await VKControls.get_token(params)
    stmt  = await ORMService().get_user_id_vk(user.get("user_id"))
    token_control = JWTControl()
    if stmt.id_vk == user.get("user_id"):
        data_tkn = {"user_name": user.get("user_id")}
        access = await token_control.create_access(data_tkn)
        refresh = await token_control.create_refresh(data_tkn)
        response.set_cookie(
        key="access", value=access, httponly=True, secure=True, samesite="none"
    )
        return {"refresh": refresh}
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
from typing import Literal

from pydantic import BaseModel

from src.config import Settings as settings


class DictLinkVK(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: int = settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE_VK
    code_challenge: str
    code_challenge_method: str = "s256"


class DictGetDataVK(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    code_verifier: str
    client_id: int = settings.VK_APP_ID
    device_id: str
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE_VK


class DictGetDataTokenVK(BaseModel):
    access_token: str
    client_id: int = settings.VK_APP_ID


class RegistrationVK(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    id_vk: int
    email: str

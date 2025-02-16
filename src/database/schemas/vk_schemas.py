from src.config import Settings as settings
from typing import Literal
from pydantic import BaseModel



class DictLinkVK(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: int = settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE_VK
    code_challenge: str = settings.VK_CODE_CHALLENGE
    code_challenge_method: str = settings.VK_CODE_CHALLENGE_METHOD


class DictGetDataVK(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    code_verifier: str = settings.VK_CODE_VERIFIER
    client_id: int = settings.VK_APP_ID
    device_id: str
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE_VK


class DictGetDataTokenVK(BaseModel):
    access_token: str
    client_id: int = settings.VK_APP_ID

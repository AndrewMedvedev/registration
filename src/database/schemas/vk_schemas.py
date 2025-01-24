from typing import Literal
from pydantic import BaseModel
from src.config import Settings as settings


class DictLinkVK(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: int = settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE_VK
    code_challenge: str = settings.VK_CODE_CHALLENGE


class DictGetDataVK(BaseModel):
    client_secret: str = settings.CLIENT_SECRET
    grant_type: Literal["authorization_code"] = "authorization_code"
    code_verifier: str = settings.VK_CODE_VERIFIER
    redirect_uri: str = settings.VK_REDIRECT_URI
    code: str
    client_id: int = settings.VK_APP_ID
    state: str = settings.STATE_VK

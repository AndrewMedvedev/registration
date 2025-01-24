from typing import Literal
from pydantic import BaseModel
from src.config import Settings as settings


class DictLinkYandex(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: str = settings.YANDEX_APP_ID
    scope: str = settings.SCOPE
    redirect_uri: str = settings.YANDEX_REDIRECT_URI
    state: str = settings.STATE_YANDEX
    code_challenge: str = settings.YANDEX_CODE_CHALLENGE
    scope: str = settings.YANDEX_SCOPE


class DictGetDataYandex(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    client_id: str = settings.YANDEX_APP_ID
    client_secret: str = settings.YANDEX_APP_SECRET
    code_verifier: str = settings.YANDEX_CODE_VERIFIER


class DictGetDataTokenYandex(BaseModel):
    oauth_token: str
    format: Literal["json"] = "json"

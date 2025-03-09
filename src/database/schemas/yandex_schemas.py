from typing import Literal

from pydantic import BaseModel

from src.config import Settings as settings


class DictLinkYandex(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: str = settings.YANDEX_APP_ID
    code_challenge: str
    code_challenge_method: str = "S256"


class DictGetDataYandex(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    client_id: str = settings.YANDEX_APP_ID
    client_secret: str = settings.YANDEX_APP_SECRET
    code_verifier: str


class DictGetDataTokenYandex(BaseModel):
    oauth_token: str
    format: Literal["json"] = "json"


class RegistrationYandex(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    id_yandex: str
    login: str
    email: str

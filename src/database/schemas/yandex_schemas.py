from typing import Literal
from pydantic import BaseModel
from src.config import Settings as settings


class DictLinkYandex(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: str = settings.YANDEX_APP_ID


class DictGetDataYandex(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    client_id: str = settings.YANDEX_APP_ID
    client_secret: str = settings.YANDEX_APP_SECRET


class DictGetDataTokenYandex(BaseModel):
    oauth_token: str
    format: Literal["json"] = "json"

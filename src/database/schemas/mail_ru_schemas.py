from typing import Literal
from pydantic import BaseModel
from src.config import Settings as settings


class DictLinkMailRu(BaseModel):
    client_id: str = settings.MAIL_RU_APP_ID
    response_type: Literal["code"] = "code"
    scope: str = settings.SCOPE
    redirect_uri: str = settings.MAIL_RU_REDIRECT_URI
    state: str = settings.STATE_MAIL_RU
    prompt_force: int = settings.PROMPT_FORCE


class DictGetDataMailRu(BaseModel):
    code: str
    grant_type: Literal["authorization_code"] = "authorization_code"
    redirect_uri: str = settings.MAIL_RU_REDIRECT_URI
    client_id: str = settings.MAIL_RU_APP_ID
    client_secret: str = settings.MAIL_RU_APP_SECRET


class DictGetDataTokenMailRu(BaseModel):
    access_token: str

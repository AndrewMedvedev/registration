from __future__ import annotations

from typing import Literal

import re
from uuid import UUID

from email_validator import validate_email
from pydantic import BaseModel, field_validator

from config import settings

from .constants import CONST_10, CONST_11
from .database.models import AdminModel, UserModel, UserVkModel, UserYandexModel
from .exeptions import BadRequestHTTPError
from .utils import Hash, format_phone_number


class AdminSchema(BaseModel):
    email: str
    hash_password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        raise BadRequestHTTPError(message="wrong email")

    def to_model(self) -> AdminModel:
        return AdminModel(
            email=self.email,
            hash_password=Hash.get_password_hash(self.hash_password),
        )


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    hash_password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        format_ph = format_phone_number(value)
        if not format_ph:
            raise BadRequestHTTPError(message="wrong phone number")
        return format_ph

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        raise BadRequestHTTPError(message="wrong email")

    def to_model(self) -> UserModel:
        return UserModel(
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            email=self.email,
            hash_password=Hash.get_password_hash(self.hash_password),
        )


class GetUserEmailSchema(BaseModel):
    email: str
    hash_password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        raise BadRequestHTTPError(message="wrong email")


class GetUserPhoneNumberSchema(BaseModel):
    phone_number: str
    hash_password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str) -> str:
        digits = re.sub(pattern=r"\D", repl="", string=phone_number)
        if len(digits) == CONST_11 and digits.startswith("8"):
            digits = "7" + digits[1:]
        elif len(digits) == CONST_10 and digits.startswith("9"):
            digits = "7" + digits
        return f"+{digits[0]}({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"


class UserDataResponse(BaseModel):
    first_name: str
    last_name: str
    email: str

    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


class GetAdminResponse(BaseModel):
    id: UUID
    hash_password: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hash_password": self.hash_password,
        }


class GetUserResponse(BaseModel):
    id: UUID
    hash_password: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hash_password": self.hash_password,
        }


class Codes(BaseModel):
    state: str
    code_verifier: str
    code_challenge: str


class Tokens(BaseModel):
    state: str
    access_token: str
    refresh_token: str

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }


class RegistrationVKSchema(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    id_vk: int
    email: str

    def to_model(self) -> UserVkModel:
        return UserVkModel(
            user_id=self.user_id,
            first_name=self.first_name,
            last_name=self.last_name,
            id_vk=self.id_vk,
            email=self.email.lower(),
        )


class RegistrationYandex(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    id_yandex: str
    login: str
    email: str

    def to_model(self) -> UserYandexModel:
        return UserYandexModel(
            user_id=self.user_id,
            first_name=self.first_name,
            last_name=self.last_name,
            id_yandex=self.id_yandex,
            login=self.login,
            email=self.email,
        )


class DictLinkVK(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: int = settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str
    code_challenge: str
    code_challenge_method: str = "s256"


class DictGetDataVK(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    code_verifier: str
    client_id: int = settings.VK_APP_ID
    device_id: str
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str


class DictGetDataTokenVK(BaseModel):
    access_token: str
    client_id: int = settings.VK_APP_ID


class DictLinkYandex(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: str = settings.YANDEX_APP_ID
    state: str
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

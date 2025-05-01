from __future__ import annotations

from typing import Literal

from uuid import UUID

import phonenumbers
from email_validator import validate_email
from pydantic import BaseModel, field_validator

from config import Settings

from .database.models import UserModel, UserVkModel, UserYandexModel
from .exeptions import BadRequestHTTPError
from .utils import Hash


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    hash_password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        raise BadRequestHTTPError(message="wrong number")

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
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        raise BadRequestHTTPError(message="wrong number")


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


class GetUserResponse(BaseModel):
    id: UUID
    hash_password: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hash_password": self.hash_password,
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
    client_id: int = Settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = Settings.VK_REDIRECT_URI
    state: str = Settings.STATE_VK
    code_challenge: str
    code_challenge_method: str = "s256"


class DictGetDataVK(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    code_verifier: str
    client_id: int = Settings.VK_APP_ID
    device_id: str
    redirect_uri: str = Settings.VK_REDIRECT_URI
    state: str = Settings.STATE_VK


class DictGetDataTokenVK(BaseModel):
    access_token: str
    client_id: int = Settings.VK_APP_ID


class DictLinkYandex(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: str = Settings.YANDEX_APP_ID
    code_challenge: str
    code_challenge_method: str = "S256"


class DictGetDataYandex(BaseModel):
    grant_type: Literal["authorization_code"] = "authorization_code"
    code: str
    client_id: str = Settings.YANDEX_APP_ID
    client_secret: str = Settings.YANDEX_APP_SECRET
    code_verifier: str


class DictGetDataTokenYandex(BaseModel):
    oauth_token: str
    format: Literal["json"] = "json"

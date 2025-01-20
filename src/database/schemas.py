from typing import Literal
from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email
from src.config import Settings as settings
from fastapi import HTTPException, status
import phonenumbers


class UserModel(BaseModel):
    phone_number: str = Field(
        default=...,
        description="Номер телефона в международном формате, начинающийся с '+'",
    )
    email: str = Field(
        default=..., min_length=5, max_length=100, description="Электронная почта "
    )
    hash_password: str = Field(default=..., description="Пароль")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Номер телефона должен начинаться с "
                + " и содержать от 1 до 15 цифр",
            )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email не соответствует формату",
            )


class GetUserEmail(BaseModel):
    email: str = Field(
        default=..., min_length=5, max_length=100, description="Электронная почта "
    )
    hash_password: str = Field(default=..., description="Пароль")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value.lower()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email не соответствует формату",
            )


class GetUserPhoneNumber(BaseModel):
    phone_number: str = Field(
        default=..., min_length=5, max_length=100, description="Номер телефона"
    )
    hash_password: str = Field(default=..., description="Пароль")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Номер телефона должен начинаться с "
                + " и содержать от 1 до 15 цифр",
            )


class DictLink(BaseModel):
    response_type: Literal["code"] = "code"
    client_id: int = settings.VK_APP_ID
    scope: Literal["email"] = "email"
    redirect_uri: str = settings.VK_REDIRECT_URI
    state: str = settings.STATE
    code_challenge: str = settings.CODE_CHALLENGE


class DictGetData(BaseModel):
    client_secret: str = settings.CLIENT_SECRET
    grant_type: Literal["authorization_code"] = "authorization_code"
    code_verifier: str = settings.CODE_VERIFIER
    redirect_uri: str = settings.VK_REDIRECT_URI
    code: str
    client_id: int = settings.VK_APP_ID
    state: str = settings.STATE

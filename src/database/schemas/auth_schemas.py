import phonenumbers
from email_validator import validate_email
from pydantic import BaseModel, Field, field_validator

from src.errors import EmailError, PhoneNumberError


class UserModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    hash_password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        try:
            parsed_number = phonenumbers.parse(values)
            if phonenumbers.is_valid_number(parsed_number):
                return values
        except Exception:
            raise PhoneNumberError(
                detail="Номер телефона должен начинаться с "
                + " и содержать от 1 до 15 цифр",
            )

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        try:
            if validate_email(value):
                return value.lower()
        except Exception:
            raise EmailError(
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
        try:
            if validate_email(value):
                return value.lower()
        except Exception:
            raise EmailError(
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
        try:
            parsed_number = phonenumbers.parse(values)
            if phonenumbers.is_valid_number(parsed_number):
                return values
        except Exception:
            raise PhoneNumberError(
                detail="Номер телефона должен начинаться с "
                + " и содержать от 1 до 15 цифр",
            )

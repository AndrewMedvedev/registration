from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email
import phonenumbers
from fastapi import HTTPException , status



class UserModel(BaseModel):
    phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    email: str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    hash_password : str = Field(default=...,description="Пароль")
    first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(default=..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    first_name_fa : str = Field(default=..., min_length=1, max_length=50, description="Отчество, от 1 до 50 символов")
    snils : str = Field(default=...,min_length=1, max_length=15,description="Снилс")
    faculty : str = Field(default=...,min_length=1, max_length=50,description="Факультет")
    number_school: str = Field(default=...,min_length=1, max_length=30,description="Номер Школы")
    class_school : str = Field(default=...,min_length=1, max_length=20,description="Класс")
    group : str = Field(default=...,min_length=1, max_length=20,description="Группа")
    
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр"
            )



    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value
        else:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email не соответствует формату"
            )


class GetUser(BaseModel):
    email:  str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    hash_password: str = Field(default=...,description="Пароль")
    
    

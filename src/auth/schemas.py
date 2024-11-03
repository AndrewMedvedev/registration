from pydantic import BaseModel, Field, field_validator
from email_validator import validate_email
import phonenumbers
import asyncpg
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from src.database import async_session_maker




class ApplicantModel(BaseModel):
    phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(default=..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    first_name_fa : str = Field(default=..., min_length=1, max_length=50, description="Отчество, от 1 до 50 символов")
    email: str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    snils : str = Field(default=...,min_length=1, max_length=15,description="Снилс")
    hash_password : str = Field(default=...,description="Пароль")
    
    
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')


    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value
        else:
            raise ValueError('email не соответствует формату')
        
        
        
        
class StudentModel(BaseModel):
    phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(default=..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    first_name_fa : str = Field(default=..., min_length=1, max_length=50, description="Отчество, от 1 до 50 символов")
    email: str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    faculty : str = Field(default=...,description="Факультет")
    group : str = Field(default=...,description="Номер группы")
    hash_password : str = Field(default=...,description="Пароль")
    

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')


    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value
        else:
            raise ValueError('email не соответствует формату')
        
        
        
        
class SchoolboyModel(BaseModel):
    phone_number: str = Field(default=..., description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: str = Field(default=..., min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    last_name: str = Field(default=..., min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    first_name_fa : str = Field(default=..., min_length=1, max_length=50, description="Отчество, от 1 до 50 символов")
    email: str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    number_school : str = Field(default=...,description="Номер школы")
    group : str = Field(default=...,description="Номер группы")
    class_school : str = Field(default=...,description="Класс")
    hash_password : str = Field(default=...,description="Пароль")
    
        
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        parsed_number = phonenumbers.parse(values)
        if phonenumbers.is_valid_number(parsed_number):
            return values
        else:
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')


    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if validate_email(value):
            return value
        else:
            raise ValueError('email не соответствует формату')
        
        
        
        
class UserModel(BaseModel):
    email:  str = Field(default=...,min_length=5, max_length=100, description="Электронная почта ")
    hash_password: str = Field(default=...,description="Пароль")
    
    
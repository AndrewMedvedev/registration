import uuid
from passlib.context import CryptContext
from fastapi import HTTPException, status, Response
from jose import jwt
from jose.exceptions import JWTError
from src.config import Settings as setting
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPass:

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class JWTControl:

    @staticmethod
    async def create_access(data: dict):
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=2) + datetime.now()
        data["mode"] = "access_token"
        return jwt.encode(data, setting.SECRET_KEY, setting.ALGORITHM)

    @staticmethod
    async def create_refresh(data: dict):
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=5) + datetime.now()
        data["mode"] = "refresh_token"
        return jwt.encode(data, setting.SECRET_KEY, setting.ALGORITHM)


class ValidateJWT:
    

    @staticmethod
    async def validate_refresh(token):
        if not token:
            return False
        else:
            try:
                refresh = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
                if "user_name" not in refresh and "mode" not in refresh:
                    return False
                if refresh["mode"] != "refresh_token":
                    return False
                return refresh["user_name"]
            except JWTError:
                return False

    @staticmethod
    async def validate_access(token):
        if not token:
            return False
        else:
            try:
                access = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
                if "user_name" not in access and "mode" not in access:
                    return False
                if access["mode"] != "access_token":
                    return False
                return True
            except JWTError:
                return False

from fastapi import HTTPException, status
from src.config import Settings as settings
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose.exceptions import JWTError
from jose import jwt
import uuid
import aiohttp


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
    async def create_access(data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=2) + datetime.now()
        data["mode"] = "access_token"
        return jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)

    @staticmethod
    async def create_refresh(data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=5) + datetime.now()
        data["mode"] = "refresh_token"
        return jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)


class ValidateJWT:

    @staticmethod
    async def validate_refresh(token) -> str:
        if not token:
            return False
        else:
            try:
                refresh = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
                if "user_name" not in refresh and "mode" not in refresh:
                    return False
                if refresh["mode"] != "refresh_token":
                    return False
                return refresh["user_name"]
            except JWTError:
                return False

    @staticmethod
    async def validate_access(token) -> bool:
        if not token:
            return False
        else:
            try:
                access = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
                if "user_name" not in access and "mode" not in access:
                    return False
                if access["mode"] != "access_token":
                    return False
                return True
            except JWTError:
                return False


class VKControls:

    async def get_token(params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.VK_TOKEN_URL, params=params, ssl=False
            ) as data:
                get_token = await data.json()
                return get_token

    async def get_user_data(params: dict) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                settings.VK_API_URL, params=params, ssl=False
            ) as user_response:
                user_data = await user_response.json()
                return user_data["response"]

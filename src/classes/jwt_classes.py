import uuid
from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from src.config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTCreate:

    def __init__(self, data: dict) -> None:
        self.data = data
        self.settings = Settings

    async def create_access(self) -> str:
        self.data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        self.data["exp"] = timedelta(hours=2) + datetime.now()
        self.data["mode"] = "access_token"
        return jwt.encode(self.data, self.settings.SECRET_KEY, self.settings.ALGORITHM)

    async def create_refresh(self) -> str:
        self.data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        self.data["exp"] = timedelta(hours=5) + datetime.now()
        self.data["mode"] = "refresh_token"
        return jwt.encode(self.data, self.settings.SECRET_KEY, self.settings.ALGORITHM)


class ValidateJWT:

    def __init__(self, token: str) -> None:
        self.token = token
        self.settings = Settings
        self.jwt_create = JWTCreate

    async def validate_refresh(self) -> dict | bool:
        try:
            refresh = jwt.decode(
                self.token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if "user_id" not in refresh and refresh.get("mode") != "refresh_token":
                return False

            data = {"user_id": refresh.get("user_id")}
            return {
                "access": await self.jwt_create(data=data).create_access(),
                "user_id": refresh.get("user_id"),
            }
        except JWTError:
            return False

    async def validate_access(self) -> dict | bool:
        try:
            access = jwt.decode(
                self.token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if "user_id" not in access and access.get("mode") != "access_token":
                return False
            return {"user_id": access.get("user_id")}
        except JWTError:
            return False

import uuid
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from src.config import Settings as settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTCreate:

    def __init__(self, data: dict) -> None:
        self.data = data

    async def create_access(self) -> str:
        self.data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        self.data["exp"] = timedelta(hours=2) + datetime.now()
        self.data["mode"] = "access_token"
        return jwt.encode(self.data, settings.SECRET_KEY, settings.ALGORITHM)

    async def create_refresh(self) -> str:
        self.data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        self.data["exp"] = timedelta(hours=5) + datetime.now()
        self.data["mode"] = "refresh_token"
        return jwt.encode(self.data, settings.SECRET_KEY, settings.ALGORITHM)


class ValidateJWT:

    def __init__(self, token: str) -> None:
        self.token = token

    async def validate_refresh(self) -> dict | bool:
        try:
            refresh = jwt.decode(
                self.token,
                settings.SECRET_KEY,
                settings.ALGORITHM,
            )
            if "user_id" not in refresh and refresh.get("mode") != "refresh_token":
                return False

            data = {"user_id": refresh.get("user_id")}
            return {
                "access": await JWTCreate(data=data).create_access(),
            }
        except JWTError:
            return False

    async def validate_access(self) -> bool:
        try:
            access = jwt.decode(
                self.token,
                settings.SECRET_KEY,
                settings.ALGORITHM,
            )
            if "user_id" not in access and access.get("mode") != "access_token":
                return False
            return True
        except JWTError:
            return False

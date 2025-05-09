import logging
import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

log = logging.getLogger(__name__)


class JWTCreate:
    def __init__(self) -> None:
        self.settings = settings

    async def create_access(self, data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=2) + datetime.now(tz=UTC)
        data["mode"] = "access_token"
        return jwt.encode(data, self.settings.SECRET_KEY, self.settings.ALGORITHM)

    async def create_refresh(self, data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
        data["exp"] = timedelta(hours=5) + datetime.now(tz=UTC)
        data["mode"] = "refresh_token"
        return jwt.encode(data, self.settings.SECRET_KEY, self.settings.ALGORITHM)

    async def create_tokens(self, user_id: UUID, role: str = "user"):
        if role != "user":
            data = {"admin": str(user_id), "role": role}
        data = {"user_id": str(user_id), "role": role}
        access = await self.create_access(data)
        refresh = await self.create_refresh(data)
        return {
            "access": access,
            "refresh": refresh,
        }


class BaseJWT(ABC):
    def __init__(self) -> None:
        self.settings = settings
        self.jwt_create = JWTCreate()

    @abstractmethod
    async def validate_refresh(self, token: str) -> dict | bool:
        raise NotImplementedError

    @abstractmethod
    async def validate_access(self, token: str) -> dict | bool:
        raise NotImplementedError

    async def valid_tokens(self, access: str, refresh: str) -> dict:
        v_refresh = await self.validate_refresh(refresh)
        v_access = await self.validate_access(access)
        if isinstance(v_access, bool):
            return v_refresh
        return v_access


class ValidateJWTUser(BaseJWT):
    async def validate_refresh(self, token: str) -> dict | bool:
        try:
            refresh = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if refresh["mode"] != "refresh_token":
                return False
            if refresh["role"] != "user":
                return False
            if "user_id" not in refresh:
                return False

            data = {"user_id": refresh["user_id"], "role": refresh["role"]}
            return {
                "access": await self.jwt_create.create_access(data=data),
                "user_id": refresh["user_id"],
            }
        except JWTError:
            return False

    async def validate_access(self, token: str) -> dict | bool:
        try:
            access = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if access["mode"] != "access_token":
                return False
            if access["role"] != "user":
                return False
            if "user_id" not in access:
                return False
            return {"user_id": access.get("user_id")}
        except JWTError:
            return False


class ValidateJWTAdmin(BaseJWT):
    async def validate_refresh(self, token: str) -> dict | bool:
        try:
            refresh = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if refresh["mode"] != "refresh_token":
                return False
            if refresh["role"] != "admin":
                return False
            if "user_id" not in refresh:
                return False

            data = {"user_id": refresh["user_id"], "role": refresh["role"]}
            return {
                "access": await self.jwt_create.create_access(data=data),
                "user_id": refresh["user_id"],
            }
        except JWTError:
            return False

    async def validate_access(self, token: str) -> dict | bool:
        try:
            access = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if access["mode"] != "access_token":
                return False
            if access["role"] != "admin":
                return False
            if "user_id" not in access:
                return False
            return {"user_id": access.get("user_id")}
        except JWTError:
            return False

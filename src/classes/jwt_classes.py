import logging
import uuid
from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from jose import jwt
from passlib.context import CryptContext

from src.config import Settings
from src.errors import JWTCreateError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

log = logging.getLogger(__name__)

class JWTCreate:

    def __init__(self) -> None:
        self.settings = Settings

    async def create_access(
        self,
        data: dict,
    ) -> str:
        try:
            data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
            data["exp"] = timedelta(hours=2) + datetime.now()
            data["mode"] = "access_token"
            return jwt.encode(data, self.settings.SECRET_KEY, self.settings.ALGORITHM)
        except JWTCreateError:
            raise JWTCreateError("create_access")

    async def create_refresh(
        self,
        data: dict,
    ) -> str:
        try:
            data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid.uuid4())}
            data["exp"] = timedelta(hours=5) + datetime.now()
            data["mode"] = "refresh_token"
            return jwt.encode(data, self.settings.SECRET_KEY, self.settings.ALGORITHM)
        except JWTCreateError:
            raise JWTCreateError("create_refresh")

    async def create_tokens(
        self,
        user_id: int,
    ) -> JSONResponse:
        try: 
            data = {"user_id": user_id}
            access = await self.create_access(data)
            refresh = await self.create_access(data)
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )
        except JWTCreateError:
            raise JWTCreateError("create_tokens")


class ValidateJWT:

    def __init__(self) -> None:
        self.settings = Settings
        self.jwt_create = JWTCreate()

    async def validate_refresh(
        self,
        token: str,
    ) -> dict | bool:
        try:
            refresh = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if "user_id" not in refresh and refresh.get("mode") != "refresh_token":
                return False

            data = {"user_id": refresh.get("user_id")}
            return {
                "access": await self.jwt_create.create_access(data=data),
                "user_id": refresh.get("user_id"),
            }
        except Exception:
            return False

    async def validate_access(self, token: str) -> dict | bool:
        try:
            access = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                self.settings.ALGORITHM,
            )
            if "user_id" not in access and access.get("mode") != "access_token":
                return False
            return {"user_id": access.get("user_id")}
        except Exception:
            return False

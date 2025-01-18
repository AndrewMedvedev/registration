from datetime import datetime, timedelta
from src.config import Settings as settings
from passlib.context import CryptContext
from jose.exceptions import JWTError
from jose import jwt
import uuid

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

    async def validate_refresh(self) -> str:
        if not self.token:
            return False
        else:
            try:
                refresh = jwt.decode(
                    self.token, settings.SECRET_KEY, settings.ALGORITHM
                )
                if "user_name" not in refresh and "mode" not in refresh:
                    return False
                if refresh["mode"] != "refresh_token":
                    return False
                return refresh["user_name"]
            except JWTError:
                return False

    async def validate_access(self) -> bool:
        if not self.token:
            return False
        else:
            try:
                access = jwt.decode(self.token, settings.SECRET_KEY, settings.ALGORITHM)
                if "user_name" not in access and "mode" not in access:
                    return False
                if access["mode"] != "access_token":
                    return False
                return True
            except JWTError:
                return False

from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.database import HashPass
from src.database.models import User
from src.services.orm import ORMService
from src.interfaces import AuthorizationBase


class Authorization(AuthorizationBase):

    def __init__(self, model) -> None:
        self.model = model
        self.orm = ORMService()
        self.jwt_create = JWTCreate
        self.hash = HashPass
        self.user = User

    async def registration(self) -> JSONResponse:
        user_model = self.user(
            first_name=self.model.first_name,
            last_name=self.model.last_name,
            phone_number=self.model.phone_number,
            email=self.model.email,
            hash_password=self.hash.get_password_hash(self.model.hash_password),
        )
        user_id = await self.orm.add_user(user_model)
        data = {"user_id": user_id}
        access = await self.jwt_create(data).create_access()
        refresh = await self.jwt_create(data).create_refresh()
        return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

    async def login_email(self) -> JSONResponse:
        stmt = await self.orm.get_user_email(
            email=self.model.email,
            hash_password=self.model.hash_password,
        )
        if (stmt.email == self.model.email) and self.hash.verify_password(
            self.model.hash_password, stmt.hash_password
        ):
            data = {"user_id": stmt.id}
            access = await self.jwt_create(data).create_access()
            refresh = await self.jwt_create(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

    async def login_phone(self) -> JSONResponse:
        stmt = await self.orm.get_user_phone_number(
            phone_number=self.model.phone_number,
            hash_password=self.model.hash_password,
        )
        if (stmt.phone_number == self.model.phone_number) and self.hash.verify_password(
            self.model.hash_password, stmt.hash_password
        ):
            data = {"user_id": stmt.id}
            access = await self.jwt_create(data).create_access()
            refresh = await self.jwt_create(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

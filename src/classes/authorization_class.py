from fastapi.responses import JSONResponse

from src.classes.jwt_classes import JWTCreate
from src.database import HashPass
from src.database.models import User
from src.services.orm import ORMService


class Authorization:

    def __init__(self, model) -> None:
        self.model = model

    async def registration(self) -> JSONResponse:
        user_model = User(
            first_name=self.model.first_name,
            last_name=self.model.last_name,
            phone_number=self.model.phone_number,
            email=self.model.email,
            hash_password=HashPass.get_password_hash(self.model.hash_password),
        )
        user_id = await ORMService().add_user(user_model)
        data = {"user_id": user_id}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return JSONResponse(
            content={
                "access": access,
                "refresh": refresh,
            }
        )

    async def login_email(self) -> JSONResponse:
        stmt = await ORMService().get_user_email(
            email=self.model.email,
            hash_password=self.model.hash_password,
        )
        if (stmt.email == self.model.email) and HashPass.verify_password(
            self.model.hash_password, stmt.hash_password
        ):
            data = {"user_id": stmt.id}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

    async def login_phone(self) -> JSONResponse:
        stmt = await ORMService().get_user_phone_number(
            phone_number=self.model.phone_number,
            hash_password=self.model.hash_password,
        )
        if (stmt.phone_number == self.model.phone_number) and HashPass.verify_password(
            self.model.hash_password, stmt.hash_password
        ):
            data = {"user_id": stmt.id}
            access = await JWTCreate(data).create_access()
            refresh = await JWTCreate(data).create_refresh()
            return JSONResponse(
                content={
                    "access": access,
                    "refresh": refresh,
                }
            )

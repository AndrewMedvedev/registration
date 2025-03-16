import logging

from fastapi.responses import JSONResponse

from src.database.models import User
from src.database.schemas import GetUserEmail, GetUserPhoneNumber, UserModel
from src.interfaces import BasicAuthorizationBase
from src.services.orm import ORMService

from .controls import HashPass
from .jwt_classes import JWTCreate

log = logging.getLogger(__name__)

class Authorization(BasicAuthorizationBase):

    def __init__(self) -> None:
        self.orm = ORMService()
        self.jwt_create = JWTCreate()
        self.hash = HashPass
        self.user = User

    async def registration(self, model: UserModel) -> JSONResponse:
        user_model = self.user(
            first_name=model.first_name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            email=model.email,
            hash_password=self.hash.get_password_hash(model.hash_password),
        )
        user_id = await self.orm.add_user(user_model)
        log.info(user_id)
        return await self.jwt_create.create_tokens(user_id)

    async def login_email(self, model: GetUserEmail) -> JSONResponse:
        stmt = await self.orm.get_user_email(
            email=model.email,
        )
        log.info(stmt)
        if (stmt.email == model.email) and self.hash.verify_password(
            model.hash_password, stmt.hash_password
        ):
            return await self.jwt_create.create_tokens(stmt.id)

    async def login_phone(self, model: GetUserPhoneNumber) -> JSONResponse:
        stmt = await self.orm.get_user_phone_number(
            phone_number=model.phone_number,
        )
        log.info(stmt)
        if (stmt.phone_number == model.phone_number) and self.hash.verify_password(
            model.hash_password, stmt.hash_password
        ):
            return await self.jwt_create.create_tokens(stmt.id)
        

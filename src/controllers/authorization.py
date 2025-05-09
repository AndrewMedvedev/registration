from ..database.crud import SQLAuthorization
from ..exeptions import BadRequestHTTPError
from ..jwt import JWTCreate
from ..schemas import AdminSchema, GetUserEmailSchema, GetUserPhoneNumberSchema, UserSchema
from ..utils import Hash


class RegistrationControl:
    def __init__(self):
        self.sql_authorization = SQLAuthorization()
        self.jwt_create = JWTCreate()

    async def registration_user(self, model: UserSchema) -> dict:
        user_id = await self.sql_authorization.create_user(model.to_model())
        return await self.jwt_create.create_tokens(user_id=user_id)

    async def registration_admin(self, model: AdminSchema) -> dict:
        user_id = await self.sql_authorization.create_admin(model.to_model())
        return await self.jwt_create.create_tokens(user_id=user_id, role="admin")


class AuthorizationControl:
    def __init__(self):
        self.sql_authorization = SQLAuthorization()
        self.jwt_create = JWTCreate()
        self.hash = Hash

    async def login_email(self, model: GetUserEmailSchema) -> dict:
        stmt = await self.sql_authorization.get_user_email(email=model.email)
        if self.hash.verify_password(model.hash_password, stmt["hash_password"]):
            return await self.jwt_create.create_tokens(stmt["id"])
        raise BadRequestHTTPError(message="wrong password")

    async def login_phone(self, model: GetUserPhoneNumberSchema) -> dict:
        stmt = await self.sql_authorization.get_user_phone_number(phone_number=model.phone_number)
        if self.hash.verify_password(model.hash_password, stmt["hash_password"]):
            return await self.jwt_create.create_tokens(stmt["id"])
        raise BadRequestHTTPError(message="wrong password")

    async def login_admin(self, model: AdminSchema) -> dict:
        stmt = await self.sql_authorization.get_admin_email(email=model.email)
        if self.hash.verify_password(model.hash_password, stmt["hash_password"]):
            return await self.jwt_create.create_tokens(stmt["id"], role="admin")
        raise BadRequestHTTPError(message="wrong password")

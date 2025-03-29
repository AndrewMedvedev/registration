from fastapi import APIRouter
from src.responses import CustomResponse

from src.classes.authorization_class import Authorization
from src.database.schemas.auth_schemas import (
    GetUserEmail,
    GetUserPhoneNumber,
    UserModel,
)

router_authorization = APIRouter(
    prefix="/api/v1/authorizations", tags=["authorization"]
)


@router_authorization.post(
    "/registration",
    response_model=None,
)
async def registration(user: UserModel) -> CustomResponse:
    return await Authorization().registration(model=user)


@router_authorization.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> CustomResponse:
    return await Authorization().login_email(model=user)


@router_authorization.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(user: GetUserPhoneNumber) -> CustomResponse:
    return await Authorization().login_phone(model=user)

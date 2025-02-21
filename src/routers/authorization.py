from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.classes.authorization_class import Authorization
from src.database.schemas.auth_schemas import (GetUserEmail,
                                               GetUserPhoneNumber, UserModel)

router_authorization = APIRouter(prefix="/authorizations/v1", tags=["authorization"])


@router_authorization.post(
    "/registration",
    response_model=None,
)
async def registration(user: UserModel) -> JSONResponse:
    try:
        return await Authorization(model=user).registration()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_authorization.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> JSONResponse:
    try:
        return await Authorization(model=user).login_email()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_authorization.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(user: GetUserPhoneNumber) -> JSONResponse:
    try:
        return await Authorization(model=user).login_phone()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

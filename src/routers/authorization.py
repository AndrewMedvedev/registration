from fastapi.responses import JSONResponse
from src.classes.authorization_class import Authorization
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from src.database.schemas.auth_schemas import (
    GetUserEmail,
    GetUserPhoneNumber,
    UserModel,
)

router = APIRouter(prefix="/authorization", tags=["authorization"])


@router.post(
    "/registration",
    response_model=None,
)
async def registration(user: UserModel) -> dict | HTTPException:
    try:
        return await Authorization(model=user).registration()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> dict | HTTPException:
    try:
        return await Authorization(model=user).login_email()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(user: GetUserPhoneNumber) -> dict | HTTPException:
    try:
        return await Authorization(model=user).login_phone()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

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
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> dict | HTTPException:
    try:
        return await Authorization(model=user).login_email()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(user: GetUserPhoneNumber) -> dict | HTTPException:
    try:
        return await Authorization(model=user).login_phone()
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

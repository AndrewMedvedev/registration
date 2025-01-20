from fastapi import APIRouter, HTTPException
from src.classes.authorization_class import Authorization
from src.database.schemas import GetUserEmail, GetUserPhoneNumber, UserModel

router = APIRouter(prefix="/authorization", tags=["authorization"])


@router.post(
    "/registration",
)
async def registration(user: UserModel) -> dict:
    return await Authorization(model=user).registration()


@router.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> dict | HTTPException:
    return await Authorization(model=user).login_email()


@router.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(user: GetUserPhoneNumber) -> dict | HTTPException:
    return await Authorization(model=user).login_phone()

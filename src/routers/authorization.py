from fastapi import APIRouter, HTTPException, status, Response
from src.classes.jwt_classes import JWTCreate
from src.database.controls import HashPass
from src.database.models import User
from src.database.schemas import GetUserEmail, GetUserPhoneNumber, UserModel
from src.services.orm import ORMService

router = APIRouter(prefix="/authorization", tags=["authorization"])


@router.post(
    "/registration",
    response_model=None,
)
async def registration(user: UserModel) -> dict:
    user_model = User(
        phone_number=user.phone_number,
        email=user.email,
        hash_password=HashPass.get_password_hash(user.hash_password),
    )
    await ORMService().add_user(user_model)
    data = {"user_name": user.email}
    access = await JWTCreate(data).create_access()
    refresh = await JWTCreate(data).create_refresh()
    return {"access": access, "refresh": refresh}


@router.post(
    "/login/email",
    response_model=None,
)
async def login(user: GetUserEmail) -> dict | HTTPException:
    stmt = await ORMService().get_user_email(
        email=user.email, hash_password=user.hash_password
    )
    if (stmt.email == user.email) and HashPass.verify_password(
        user.hash_password, stmt.hash_password
    ):
        data = {"user_name": user.email}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return {"access": access, "refresh": refresh}
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post(
    "/login/phone/number",
    response_model=None,
)
async def login(user: GetUserPhoneNumber) -> dict | HTTPException:
    stmt = await ORMService().get_user_phone_number(
        phone_number=user.phone_number, hash_password=user.hash_password
    )
    if (stmt.phone_number == user.phone_number) and HashPass.verify_password(
        user.hash_password, stmt.hash_password
    ):
        data = {"user_name": stmt.email}
        access = await JWTCreate(data).create_access()
        refresh = await JWTCreate(data).create_refresh()
        return {"access": access, "refresh": refresh}
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post(
    "/logout",
    response_model=None,
)
async def logout(response: Response) -> HTTPException:
    response.delete_cookie(key="access")
    response.delete_cookie(key="refresh")
    return HTTPException(status_code=status.HTTP_200_OK)

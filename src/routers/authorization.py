from fastapi import APIRouter, HTTPException, status, Response
from src.database.controls import HashPass, JWTControl
from src.database.models import User
from src.database.schemas import GetUserEmail, GetUserPhoneNumber, UserModel
from src.services.orm import ORMService

router = APIRouter(prefix="/authorization", tags=["authorization"])


@router.post("/registration")
async def registration(user: UserModel, response: Response) -> dict:
    user_model = User(
        phone_number=user.phone_number,
        email=user.email,
        hash_password=HashPass.get_password_hash(user.hash_password),
    )
    token_control = JWTControl()
    await ORMService().add_user(user_model)
    data = {"user_name": user.email}
    access = await token_control.create_access(data)
    refresh = await token_control.create_refresh(data)
    response.set_cookie(
        key="access", value=access, httponly=True, secure=True, samesite="none"
    )
    return {"refresh": refresh}


@router.post("/login/email")
async def login(user: GetUserEmail, response: Response) -> dict:
    stmt = await ORMService().get_user_email(
        email=user.email, hash_password=user.hash_password
    )
    if (stmt.email == user.email) and HashPass.verify_password(
        user.hash_password, stmt.hash_password
    ):
        data = {"user_name": user.email}
        token_control = JWTControl()
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response.set_cookie(
            key="access", value=access, httponly=True, secure=True, samesite="none"
        )
        return {"refresh": refresh}
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/login/phone/number")
async def login(user: GetUserPhoneNumber, response: Response) -> dict:
    stmt = await ORMService().get_user_phone_number(
        phone_number=user.phone_number, hash_password=user.hash_password
    )
    if (stmt.phone_number == user.phone_number) and HashPass.verify_password(
        user.hash_password, stmt.hash_password
    ):
        data = {"user_name": stmt.email}
        token_control = JWTControl()
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response.set_cookie(
            key="access", value=access, httponly=True, secure=True, samesite="none"
        )
        return {"refresh": refresh}
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/logout")
async def logout(response: Response) -> HTTPException:
    response.delete_cookie(key="access")
    return HTTPException(status_code=status.HTTP_200_OK)

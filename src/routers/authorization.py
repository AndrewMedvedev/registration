from fastapi import APIRouter, HTTPException, status, Response
from auth.controls import HashPass, JWTControl
from auth.models import User
from auth.schemas import GetUser, UserModel
from services.orm import ORMService

router = APIRouter(prefix="/authorization", tags=["authorization"])


@router.post("/registration")
async def registration(user: UserModel, response: Response):
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


@router.post("/login")
async def login(user: GetUser, response: Response):
    stmt = await ORMService().get_user(
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


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access")
    return HTTPException(status_code=status.HTTP_200_OK)

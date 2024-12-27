from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from src.auth.schemas import UserModel, GetUser
from src.auth.controls import JWTControl, HashPass, ValidateJWT
from src.services.orm import ORMService
from src.auth.models import User
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address, default_limits=["10/second"])
app = FastAPI(title="Регистрация")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/registration")
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


@app.post("/login")
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


@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access")
    return HTTPException(status_code=status.HTTP_200_OK)


@app.post("/validate_tokens/jwt")
async def validate_access(refresh: str, request: Request, response: Response):
    tkn_refresh = await ValidateJWT.validate_refresh(refresh)
    access = request.cookies.get("access")
    tkn_access = await ValidateJWT.validate_access(access)
    if tkn_access != False:
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
        if tkn_refresh != False:
            token_control = JWTControl()
            data = {"user_name": tkn_refresh}
            access = await token_control.create_access(data)
            response.set_cookie(
                key="access", value=access, httponly=True, secure=True, samesite="none"
            )
            return HTTPException(status_code=status.HTTP_200_OK)
        else:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

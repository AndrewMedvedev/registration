from fastapi import FastAPI, Response , Request , HTTPException, status , Depends 
from fastapi.responses import RedirectResponse
from src.auth.schemas import UserModel , GetUser 
from src.auth.controls import JWTControl , HashPass , ValidateJWT
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




@app.post('/registration')
async def registration(user: UserModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
                phone_number=user.phone_number,
                email=user.email,
                hash_password=HashPass.get_password_hash(user.hash_password)
            )
        token_control = JWTControl()
        await ORMService().add_user(user_model)
        data = {'user_name': user.email}
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response.set_cookie(key='refresh',value=refresh)
        response.set_cookie(key='access',value=access)
        return HTTPException(
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно введены данные"
            )


@app.post('/login')    
async def login(user: GetUser,response: Response):
    stmt = await ORMService().get_user(email=user.email,hash_password=user.hash_password)
    if (stmt.email == user.email) and HashPass.verify_password(user.hash_password, stmt.hash_password):
        data = {'user_name': user.email}
        token_control = JWTControl()
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response.set_cookie(key='refresh',value=refresh)
        response.set_cookie(key='access',value=access)
        return HTTPException(
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access')
    response.delete_cookie(key='refresh')
    return HTTPException(
            status_code=status.HTTP_200_OK
        )
    

# @app.middleware("http")
# async def notlog(request: Request):
#     access = request.cookies.get('access')
#     refresh = request.cookies.get('refresh')
#     if not refresh:
#         return RedirectResponse('/login')


@app.post('/validate/jwt')
async def validate_jwt(request: Request):
    access = request.cookies.get('access')
    refresh = request.cookies.get('refresh')
    return await ValidateJWT.validate_access(access) , await ValidateJWT.validate_refresh(refresh)
    
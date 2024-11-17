from fastapi import FastAPI, Response , Request , HTTPException, status , Depends 
from fastapi.responses import JSONResponse , RedirectResponse
from src.auth.schemas import UserModel , GetUser 
from src.auth.controls import JWTControl , HashPass , ValidateJWT
from src.services.orm import ORMService
from src.auth.models import User


app = FastAPI(
    title="Регистрация"
)


@app.post('/registration')
async def registration(user: UserModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
                first_name=user.first_name,
                last_name=user.last_name,
                first_name_fa=user.first_name_fa,
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
    raise HTTPException(
                status_code=status.HTTP_200_OK,
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
    
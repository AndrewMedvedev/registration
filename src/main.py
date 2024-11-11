from fastapi import FastAPI, Response , Request , HTTPException, status , Depends 
from fastapi.responses import JSONResponse , RedirectResponse
from src.auth.schemas import UserModel , GetUser 
from src.auth.controls import JWTControl , HashPass
from src.services.orm import ORMService
from src.auth.models import User

app = FastAPI(
    title="Регистрация"
)


@app.post('/registration')
async def registration(user: UserModel,_: Request) -> Response:
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
            phone_number=user.phone_number,
            email=user.email,
            hash_password=HashPass.get_password_hash(user.hash_password),
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            snils=user.snils,
            faculty=user.faculty,
            number_school=user.number_school,
            class_school=user.class_school,
            group=user.group,
        )
        token_control = JWTControl()
        await ORMService().add_user(user_model)
        data = {'user_name': user.email}
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response = JSONResponse({
                'access':access
                })
        response.set_cookie(key='refresh',value=refresh)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно введены данные"
            )


@app.post('/login')    
async def login(user: GetUser,request: Request) -> Response:
    stmt = await ORMService().get_user(email=user.email,hash_password=user.hash_password)
    if (stmt.email == user.email) and HashPass.verify_password(user.hash_password, stmt.hash_password):
        data = {'user_name': user.email}
        token_control = JWTControl()
        access = await token_control.create_access(data)
        refresh = await token_control.create_refresh(data)
        response = JSONResponse({
                'access':access
                })
        response.set_cookie(key='refresh',value=refresh)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )


@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access")
    response.delete_cookie(key="refresh")
    raise HTTPException(
                status_code=status.HTTP_200_OK,
                )
    


# @app.middleware("http")
# async def notlog(request: Request, call_next):
#     refresh = request.cookies.get('refresh')
#     access = request.cookies.get('access')
#     if not access and :
        
#         return RedirectResponse('/login')

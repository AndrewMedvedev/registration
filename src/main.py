from fastapi import FastAPI, Response , Request , HTTPException, status , Depends 
from fastapi.responses import JSONResponse , RedirectResponse
from src.auth.schemas import UserModel , GetUser 
from src.auth.controls import JWTControl , HashPass , DatabaseControl , UserControl , ValidateJWT
from src.services.orm import ORMService

app = FastAPI(
    title="Регистрация"
)


@app.post('/registration')
async def registration(user: UserModel,_: Request) -> Response:
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        db = DatabaseControl()
        user_model = await db.validate_db(user)
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
async def login(user: GetUser) -> Response:
    model = await UserControl.check_user(user)
    stmt = await ORMService().get_user(model=model ,email=user.email,hash_password=user.hash_password)
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
    response.delete_cookie(key="refresh")
    raise HTTPException(
                status_code=status.HTTP_200_OK,
                )
    


# @app.middleware("http")
# async def notlog(request: Request, call_next):
#     refresh = request.cookies.get('refresh')
#     if not refresh:
#         return RedirectResponse('/login')

@app.post('/refresh')
async def tok(request: Request):
    tkn = request.cookies.get('refresh')
    return await ValidateJWT.validate_refresh(tkn)
    
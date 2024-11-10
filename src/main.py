from fastapi import FastAPI, Response , Request , HTTPException, status , Depends 
from fastapi.responses import JSONResponse , RedirectResponse
from src.auth.schemas import UserModel , GetUser , ApplicantModel , SchoolboyModel , StudentModel
from src.auth.controls import create_refresh ,create_access , verify_password, get_password_hash 
from src.services.orm import ORMService
from src.auth.models import User

app = FastAPI(
    title="Регистрация"
)


@app.post('/registration/applicant')
async def registration_applicant(user: ApplicantModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            snils=user.snils,
            hash_password=get_password_hash(user.hash_password),
            faculty="None",
            number_school="None",
            class_school="None",
            group="None"
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        response.set_cookie(key="refresh", value=refresh_tkn, httponly=True)
        return HTTPException(
                status_code=status.HTTP_200_OK,
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно введены данные"
            )


@app.post('/registration/student')
async def registration_student(user: StudentModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            faculty=user.faculty,
            group=user.group,
            hash_password=get_password_hash(user.hash_password),
            number_school="None",
            class_school="None",
            snils="None"
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        response.set_cookie(key="refresh", value=refresh_tkn, httponly=True)
        return HTTPException(
                status_code=status.HTTP_200_OK,
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно введены данные"
            )


@app.post('/registration/schoolboy')
async def registration_schoolboy(user: SchoolboyModel, response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = User(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            number_school=user.number_school,
            class_school=user.class_school,
            hash_password=get_password_hash(user.hash_password),
            faculty="None",
            group="None",
            snils="None"
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        response.set_cookie(key="refresh", value=refresh_tkn, httponly=True)
        return HTTPException(
                status_code=status.HTTP_200_OK,
                )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильно введены данные"
            )
        

@app.post('/login')    
async def login(user: GetUser,request: Request,response: Response):
    stmt = await ORMService().get_user(email=user.email,hash_password=user.hash_password)
    if (stmt.email == user.email) and verify_password(user.hash_password, stmt.hash_password):
        data = {'user_name': user.email}
        response.set_cookie(key="access", value=create_access(data), httponly=True)
        response.set_cookie(key="refresh", value=create_refresh(data), httponly=True)
        return HTTPException(
                status_code=status.HTTP_200_OK,
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

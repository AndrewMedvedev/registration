from fastapi import FastAPI, Response , Request
from fastapi.responses import JSONResponse
from src.auth.schemas import ApplicantModel, SchoolboyModel, StudentModel, UserModel
from src.auth.controls import create_refresh ,create_access , verify_password, get_password_hash ,verified_user ,update_token
from src.services.orm import ORMService
from src.auth.models import Applicant , Student, Schoolboy


app = FastAPI(
    title="Регистрация"
)


@app.post('/registration/applicant')
async def registration_applicant(user: ApplicantModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = Applicant(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            snils=user.snils,
            hash_password=get_password_hash(user.hash_password)
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        return {"access": access_tkn , "refresh": refresh_tkn}
        

@app.post('/registration/student')
async def registration_student(user: StudentModel,response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = Student(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            faculty=user.faculty,
            group=user.group,
            hash_password=get_password_hash(user.hash_password)
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        return {"access": access_tkn , "refresh": refresh_tkn}


@app.post('/registration/schoolboy')
async def registration_schoolboy(user: SchoolboyModel, response: Response):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        user_model = Schoolboy(
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_fa=user.first_name_fa,
            email=user.email,
            number_school=user.number_school,
            group=user.group,
            class_school=user.class_school,
            hash_password=get_password_hash(user.hash_password)
        )
        await ORMService().add_user(user_model)
        tkn = {'user_name': user.email}
        access_tkn = create_access(tkn)
        refresh_tkn = create_refresh(tkn)
        response.set_cookie(key="access", value=access_tkn, httponly=True)
        return {"access": access_tkn , "refresh": refresh_tkn}


@app.post('/login/applicant')    
async def login(user: UserModel,request: Request,response: Response):
    stmt = await ORMService().get_user_applicant(email=user.email,hash_password=user.hash_password)
    token = request.cookies.get('access')
    if (stmt.email == user.email) and verify_password(user.hash_password, stmt.hash_password):
        if not token:
            tkn = update_token(user,token)
            response.set_cookie(key="access", value=tkn, httponly=True)
            return {"message":"Вы Авторизованны"}
        else:
            if verified_user(user,token):
                return {"message":"Вы Авторизованны"}
    else:
        return {"message":"Неверные данные"}


@app.post('/login/student')    
async def login(user: UserModel,request: Request,response: Response):
    stmt = await ORMService().get_user_student(email=user.email,hash_password=user.hash_password)
    token = request.cookies.get('access')
    if (stmt.email == user.email) and verify_password(user.hash_password, stmt.hash_password):
        if not token:
            tkn = update_token(user,token)
            response.set_cookie(key="access", value=tkn, httponly=True)
            return {"message":"Вы Авторизованны"}
        else:
            if verified_user(user,token):
                return {"message":"Вы Авторизованны"}
    else:
        return {"message":"Неверные данные"}


@app.post('/login/schoolboy')    
async def login(user: UserModel,request: Request,response: Response):
    stmt = await ORMService().get_user_schoolboy(email=user.email,hash_password=user.hash_password)
    token = request.cookies.get('access')
    if (stmt.email == user.email) and verify_password(user.hash_password, stmt.hash_password):
        if not token:
            tkn = update_token(user,token)
            response.set_cookie(key="access", value=tkn, httponly=True)
            return {"message":"Вы Авторизованны"}
        else:
            if verified_user(user,token):
                return {"message":"Вы Авторизованны"}
    else:
        return {"message":"Неверные данные"}


@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access")
    return {'message': 'Пользователь успешно вышел из системы'}
    
    
    


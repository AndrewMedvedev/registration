from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from src.auth.schemas import Applicant, Schoolboy, Student, User
from src.auth.controls import create_refresh ,create_access


app = FastAPI(
    title="Регистрация"
)


@app.post('/registration/applicant')
async def registration_applicant(user: Applicant ):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        data = {'user_name': user.email}
        access_tkn = create_access(data)
        refresh_tkn = create_refresh(data)
        return {"access": access_tkn , "refresh": refresh_tkn}
        

@app.post('/registration/student')
async def registration_student(user: Student):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        data = {'user_name': user.email}
        access_tkn = create_access(data)
        refresh_tkn = create_refresh(data)
        return {"access": access_tkn , "refresh": refresh_tkn}


@app.post('/registration/schoolboy')
async def registration_schoolboy(user: Schoolboy):
    if user.validate_phone_number(user.phone_number) and user.validate_email(user.email):
        data = {'user_name': user.email}
        access_tkn = create_access(data)
        refresh_tkn = create_refresh(data)
        return {"access": access_tkn , "refresh": refresh_tkn}


# @app.post('/login')    
# async def login(user: User):
    



@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access")
    return {'message': 'Пользователь успешно вышел из системы'}
    
    
    
    

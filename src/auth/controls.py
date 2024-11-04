from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from src.config import Settings as setting
import datetime  
from datetime import datetime , timedelta
from fastapi import Response


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/token')



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access(data: dict):
    data["header"] = { "alg": "HS256", "typ": "JWT"}
    data["exp"] = timedelta(days=1) + datetime.now()
    data["mode"] = "access_token"
    return jwt.encode(data,setting.SECRET_KEY,setting.ALGORITHM)
    
    
def create_refresh(data: dict):
    data["header"] = { "alg": "HS256", "typ": "JWT"}
    data["exp"] = timedelta(days=365) + datetime.now()
    data["mode"] = "refresh_token"
    return jwt.encode(data,setting.SECRET_KEY,setting.ALGORITHM)


async def update_token(user ,token: str = Depends(oauth_scheme)) -> dict:

    try:
        data = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)

        if 'user_name' not in data and 'mode' not in data:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )
        if data['mode'] != 'refresh_token':
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )

        user = await user.filter(email=data['user_name']).first()
        if not user or token != user.refresh_token:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )

        data = {'user_name': user.email}
        refresh_tkn = create_refresh(data)
        await user.filter(email=user.email).update(**{'refresh_token': refresh_tkn})

        access_tkn = create_access(data)
        return {
            'access_token': access_tkn,
            'refresh_token': refresh_tkn,
            'type': 'bearer'
        }
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )


async def verified_user(user ,token: str = Depends(oauth_scheme)):

    try:
        data = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)

        if 'user_name' not in data and 'mode' not in data:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )
        if data['mode'] != 'access_token':
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )

        user = await user.filter(email=data['user_name']).first()
        if not user:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )

        return user
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Вы не прошли авторизацию'
        )



    
    

    

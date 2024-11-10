from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status , Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from src.config import Settings as setting
import datetime  
from datetime import datetime , timedelta
from src.auth.schemas import GetUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access(data: dict):
    data["header"] = { "alg": "HS256", "typ": "JWT"}
    data["exp"] = timedelta(hours=5) + datetime.now()
    data["mode"] = "access_token"
    return jwt.encode(data,setting.SECRET_KEY,setting.ALGORITHM)
    
    
def create_refresh(data: dict):
    data["header"] = { "alg": "HS256", "typ": "JWT"}
    data["exp"] = timedelta(days=5) + datetime.now()
    data["mode"] = "refresh_token"
    return jwt.encode(data,setting.SECRET_KEY,setting.ALGORITHM)
    
    
async def validate_access(request:Request):
    try:
        access = jwt.decode(request.cookies.get('access'),setting.SECRET_KEY,setting.ALGORITHM)
        if 'user_name' not in access and 'mode' not in access:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        if access['mode'] != 'access_token':
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        user = await GetUser.filter(email=access['user_name']).first()
        if not user:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        return user
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )


async def validate_refresh(request:Request):
    try:
        refresh = jwt.decode(request.cookies.get('refresh'),setting.SECRET_KEY,setting.ALGORITHM)
        if 'user_name' not in refresh and 'mode' not in refresh:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        if refresh['mode'] != 'access_token':
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        user = await GetUser.filter(email=refresh['user_name']).first()
        if not user:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        return user
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        )
        
        
        
            



    
    

    

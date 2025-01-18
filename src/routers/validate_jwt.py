from fastapi import APIRouter, HTTPException, status, Request, Response
from src.classes.jwt_classes import JWTCreate, ValidateJWT

router = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router.post("/refresh")
async def validate_refresh(refresh: str, response: Response):
    tkn_refresh = await ValidateJWT(refresh).validate_refresh()
    if tkn_refresh != False:
        data = {"user_name": tkn_refresh}
        access = await JWTCreate(data).create_access()
        response.set_cookie(
            key="access", value=access, httponly=True, secure=True, samesite="none"
        )
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/access")
async def validate_access(request: Request):
    access = request.cookies.get("access")
    tkn_access = await ValidateJWT(access).validate_access()
    if tkn_access != False:
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

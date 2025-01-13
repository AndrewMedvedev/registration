from fastapi import APIRouter, HTTPException, status, Request, Response
from src.database.controls import JWTControl, ValidateJWT

router = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router.post("/refresh")
async def validate_refresh(refresh: str, response: Response) -> HTTPException:
    tkn_refresh = await ValidateJWT.validate_refresh(refresh)
    if tkn_refresh != False:
        token_control = JWTControl()
        data = {"user_name": tkn_refresh}
        access = await token_control.create_access(data)
        response.set_cookie(
            key="access", value=access, httponly=True, secure=True, samesite="none"
        )
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/access")
async def validate_access(request: Request) -> HTTPException:
    access = request.cookies.get("access")
    tkn_access = await ValidateJWT.validate_access(access)
    if tkn_access != False:
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

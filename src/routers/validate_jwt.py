from fastapi import APIRouter, HTTPException, status, Request, Response
from auth.controls import JWTControl, ValidateJWT

router = APIRouter(prefix="/validate_jwt", tags=["validate_jwt"])


@router.post("/validate_tokens/jwt")
async def validate_access(refresh: str, request: Request, response: Response):
    tkn_refresh = await ValidateJWT.validate_refresh(refresh)
    access = request.cookies.get("access")
    tkn_access = await ValidateJWT.validate_access(access)
    if tkn_access != False:
        return HTTPException(status_code=status.HTTP_200_OK)
    else:
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

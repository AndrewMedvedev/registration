from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..jwt import ValidateJWTAdmin, ValidateJWTUser

validate_jwt = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@validate_jwt.get("/user/{access}/{refresh}")
async def validate_user(access: str, refresh: str) -> JSONResponse:
    content = await ValidateJWTUser().valid_tokens(access=access, refresh=refresh)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@validate_jwt.get("/admin/{access}/{refresh}")
async def validate_admin(access: str, refresh: str) -> JSONResponse:
    content = await ValidateJWTAdmin().valid_tokens(access=access, refresh=refresh)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

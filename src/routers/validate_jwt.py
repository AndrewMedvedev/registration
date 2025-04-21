from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..jwt import ValidateJWT

validate_jwt = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@validate_jwt.get("/refresh/{refresh}")
async def validate_refresh(
    refresh: str,
) -> JSONResponse:
    content = await ValidateJWT().validate_refresh(refresh)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@validate_jwt.get("/access/{access}")
async def validate_access(
    access: str,
) -> JSONResponse:
    content = await ValidateJWT().validate_access(access)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

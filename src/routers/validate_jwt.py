from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..jwt import ValidateJWT

validate_jwt = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@validate_jwt.get("/{access}/{refresh}")
async def validate(
    access: str,
    refresh: str,
) -> JSONResponse:
    content = await ValidateJWT().valid_tokens(access=access, refresh=refresh)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

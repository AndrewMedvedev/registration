from src.classes.jwt_classes import ValidateJWT
from fastapi import APIRouter


router_validate_jwt = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router_validate_jwt.get(
    "/refresh",
    response_model=None,
)
async def validate_refresh(
    refresh: str,
) -> str | bool:
    return await ValidateJWT(refresh).validate_refresh()


@router_validate_jwt.get(
    "/access",
    response_model=None,
)
async def validate_access(
    access: str,
) -> dict | bool:
    return await ValidateJWT(access).validate_access()

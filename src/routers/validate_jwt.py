from fastapi import APIRouter, HTTPException, status
from src.classes.jwt_classes import JWTCreate, ValidateJWT

router = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router.get(
    "/refresh",
    response_model=None,
)
async def validate_refresh(
    refresh: str,
) -> str | bool:
    return await ValidateJWT(refresh).validate_refresh()
    


@router.get("/access")
async def validate_access(
    access: str,
) -> str | bool:
    return await ValidateJWT(access).validate_access()

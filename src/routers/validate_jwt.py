from fastapi import APIRouter, HTTPException, status
from src.classes.jwt_classes import JWTCreate, ValidateJWT

router = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router.post(
    "/refresh",
    response_model=None,
)
async def validate_refresh(
    refresh: str,
) -> dict | HTTPException:
    tkn_refresh = await ValidateJWT(refresh).validate_refresh()
    if tkn_refresh != False:
        data = {"user_name": tkn_refresh}
        access = await JWTCreate(data).create_access()
        return {"access": access}
    else:
        False


@router.post("/access")
async def validate_access(
    access: str,
) -> str | bool:
    return await ValidateJWT(access).validate_access()

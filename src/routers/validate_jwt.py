from fastapi import APIRouter, HTTPException, status
from src.classes.jwt_classes import JWTCreate, ValidateJWT

router = APIRouter(prefix="/validate/jwt", tags=["validate/jwt"])


@router.post("/refresh")
async def validate_refresh(
    refresh: str,
) -> dict | HTTPException:
    tkn_refresh = await ValidateJWT(refresh).validate_refresh()
    try:
        if tkn_refresh != False:
            data = {"user_name": tkn_refresh}
            access = await JWTCreate(data).create_access()
            return {"access": access}
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)




@router.post("/access")
async def validate_access(
    access: str,
) -> bool:
    tkn_access = await ValidateJWT(access).validate_access()
    if tkn_access != False:
        return True
    else:
        False

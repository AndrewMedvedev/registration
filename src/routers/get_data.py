from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.classes import GetUserData

router_data = APIRouter(prefix="/api/v1/get", tags=["get_data"])


@router_data.get("data/{user_id}")
async def get_data(
    user_id: int,
) -> JSONResponse:
    try:
        return await GetUserData(user_id=user_id).get_data()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )


@router_data.get("number/{phone_number}")
async def get_number(
    phone_number: str,
) -> JSONResponse:
    try:
        return await GetUserData(phone_number=phone_number).get_number()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

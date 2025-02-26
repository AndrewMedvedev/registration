from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.classes import GetUser

router_data = APIRouter(prefix="/api/v1/get", tags=["get_data"])


@router_data.get("/{user_id}")
async def get(
    user_id: int,
) -> JSONResponse:
    try:
        return await GetUser(user_id=user_id).get()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

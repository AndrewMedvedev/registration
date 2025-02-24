from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.classes import GetUser

router_data = APIRouter(prefix="/get/v1", tags=["get_data"])


@router_data.get("/")
async def get(user_id: int, password: str) -> JSONResponse:
    try:
        return await GetUser(user_id=user_id, password=password).get()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)}
        )

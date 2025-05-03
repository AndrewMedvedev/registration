from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import GetUserDataControl

data = APIRouter(prefix=f"{PATH_ENDPOINT}get", tags=["get_data"])


@data.get("data/{user_id}")
async def get_data(user_id: UUID) -> JSONResponse:
    content = await GetUserDataControl().get_data(user_id=user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@data.get("number/{phone_number}")
async def get_number(phone_number: str) -> JSONResponse:
    content = await GetUserDataControl().get_number(phone_number=phone_number)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

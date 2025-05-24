from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import VKControl
from ..schemas import RegistrationVKSchema

vk = APIRouter(prefix=f"{PATH_ENDPOINT}vk", tags=["vk"])


@vk.get("/link")
async def vk_link() -> JSONResponse:
    content = await VKControl().link()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@vk.post("/registration/")
async def vk_registration(model: RegistrationVKSchema) -> Response:
    await VKControl().registration(model=model)
    return Response(status_code=status.HTTP_201_CREATED)


@vk.post("/login/{code}/{device_id}/{state}")
async def vk_login(code: str, device_id: str, state: str) -> JSONResponse:
    content = await VKControl().login(code=code, device_id=device_id, state=state)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

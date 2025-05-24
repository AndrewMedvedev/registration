from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse, RedirectResponse

from ..constants import PATH_ENDPOINT
from ..controllers import VKControl
from ..schemas import RegistrationVKSchema

vk = APIRouter(prefix=f"{PATH_ENDPOINT}vk", tags=["vk"])


@vk.get("/link")
async def vk_link() -> JSONResponse:
    content = await VKControl().link()
    print(content)
    return RedirectResponse(url=content)
    # return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@vk.get("/get/token/{code}/{device_id}/{code_verifier}")
async def vk_get_token(code: str, device_id: str, code_verifier: str) -> JSONResponse:
    content = await VKControl().get_token(
        code=code, device_id=device_id, code_verifier=code_verifier
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@vk.post("/registration/")
async def vk_registration(model: RegistrationVKSchema) -> Response:
    await VKControl().registration(model=model)
    return Response(status_code=status.HTTP_201_CREATED)


@vk.post("/login/{access_token}")
async def vk_login(access_token: str) -> JSONResponse:
    content = await VKControl().login(access_token=access_token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@vk.get("/check/return")
async def check_return(code: str, state: str, device_id: str) -> tuple:
    print(code, state, device_id)
    return (code, state, device_id)

from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import YandexControl
from ..schemas import RegistrationYandex

yandex = APIRouter(prefix=f"{PATH_ENDPOINT}yandex", tags=["yandex"])


@yandex.get("/link")
async def yandex_link() -> JSONResponse:
    content = await YandexControl().link()
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@yandex.post("/registration/")
async def yandex_registration(model: RegistrationYandex) -> Response:
    await YandexControl().registration(model=model)
    return Response(status_code=status.HTTP_201_CREATED)


@yandex.post("/login/{code}/{state}")
async def yandex_login(code: str, state: str) -> JSONResponse:
    content = await YandexControl().login(code=code, state=state)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

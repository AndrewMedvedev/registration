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


@yandex.get("/get/token/{code}/{code_verifier}")
async def yandex_get_token(code: str, code_verifier: str) -> JSONResponse:
    content = await YandexControl().get_token(code=code, code_verifier=code_verifier)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@yandex.post(
    "/registration/",
)
async def yandex_registration(model: RegistrationYandex) -> Response:
    await YandexControl().registration(model=model)
    return Response(status_code=status.HTTP_201_CREATED)


@yandex.post("/login/{access_token}")
async def yandex_login(access_token: str) -> JSONResponse:
    content = await YandexControl().login(access_token=access_token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

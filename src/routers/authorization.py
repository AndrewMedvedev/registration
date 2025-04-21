from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import AuthorizationControl
from ..schemas import GetUserEmailSchema, GetUserPhoneNumberSchema, UserSchema

authorization = APIRouter(prefix=f"{PATH_ENDPOINT}authorizations", tags=["authorization"])


@authorization.post(
    "/registration",
)
async def registration(model: UserSchema) -> JSONResponse:
    content = await AuthorizationControl().registration(model=model)
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@authorization.post(
    "/login/email",
)
async def login(model: GetUserEmailSchema) -> JSONResponse:
    content = await AuthorizationControl().login_email(model=model)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@authorization.post(
    "/login/phone/number",
    response_model=None,
)
async def login_phone(model: GetUserPhoneNumberSchema) -> JSONResponse:
    content = await AuthorizationControl().login_phone(model=model)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)

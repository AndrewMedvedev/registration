from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from ..constants import PATH_ENDPOINT
from ..controllers import AuthorizationControl, RegistrationControl, ReplacePasswordControl
from ..schemas import (
    AdminSchema,
    GetUserEmailSchema,
    GetUserPhoneNumberSchema,
    ReplacePasswordSchema,
    UserSchema,
)

authorization = APIRouter(prefix=f"{PATH_ENDPOINT}authorizations", tags=["authorization"])


@authorization.post("/registration")
async def registration(model: UserSchema) -> JSONResponse:
    content = await RegistrationControl().registration_user(model=model)
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@authorization.post("/registration/admin")
async def registration_admin(model: AdminSchema) -> JSONResponse:
    content = await RegistrationControl().registration_admin(model=model)
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@authorization.post("/login/email")
async def login(model: GetUserEmailSchema) -> JSONResponse:
    content = await AuthorizationControl().login_email(model=model)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@authorization.post("/login/email/admin")
async def login_admin(model: AdminSchema) -> JSONResponse:
    content = await AuthorizationControl().login_admin(model=model)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@authorization.post("/login/phone/number")
async def login_phone(model: GetUserPhoneNumberSchema) -> JSONResponse:
    content = await AuthorizationControl().login_phone(model=model)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@authorization.patch("/replace/password")
async def replace_password(model: ReplacePasswordSchema) -> Response:
    await ReplacePasswordControl().replace_password(schema=model)
    return Response(status_code=status.HTTP_200_OK)

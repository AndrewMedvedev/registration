import base64
import hashlib
import logging
import os
from typing import Any

from aiohttp import ClientSession
from passlib.context import CryptContext

from src.errors import SendError
from src.errors.errors import PasswordError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

log = logging.getLogger(__name__)


class HashPass:

    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if answer := pwd_context.verify(plain_password, hashed_password):
            return answer
        raise PasswordError("verify_password")


class Send:

    def __init__(self):
        self.clientsession = ClientSession

    async def get_data(
        self,
        params: dict,
        setting: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.get(
                url=setting,
                params=params,
                ssl=False,
            ) as data:
                return await valid_answer(response=data, name_func="get_data")

    async def post_data(
        self,
        params: dict,
        setting: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                url=setting,
                json=params,
                ssl=False,
            ) as data:
                return await valid_answer(response=data, name_func="post_data")

    async def post_data_yandex(
        self,
        params: dict,
        setting: str,
    ) -> dict:
        async with self.clientsession() as session:
            async with session.post(
                url=setting,
                data=params,
                ssl=False,
            ) as data:
                return await valid_answer(response=data, name_func="post_data_yandex")


async def create_codes() -> dict:
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(64)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }


async def valid_answer(
    response: Any,
    name_func: str,
):
    try:
        log.warning(await response.text())
        if response.status == 200:
            data_dict = await response.json()
            log.warning(data_dict)
            return data_dict
        else:
            raise SendError(detail=f"Ошибка получения данных в функции {name_func}")
    except Exception:
        raise SendError(detail=f"Ошибка получения данных в функции {name_func}")


def config_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


# async def get_token_user_mail_ru(params: dict) -> dict:
#     async with aiohttp.ClientSession() as session:
#         async with session.post(
#             url=Settings.MAIL_RU_TOKEN_URL,
#             data=params,
#             ssl=False,
#         ) as data:
#             user_data = await data.json()
#             return user_data


# async def get_data_user_mail_ru(params: dict) -> dict:
#     async with aiohttp.ClientSession() as session:
#         async with session.get(
#             Settings.MAIL_RU_API_URL,
#             params=params,
#             ssl=False,
#         ) as data:
#             user_data = await data.json()
#             return user_data

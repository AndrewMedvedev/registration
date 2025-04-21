from typing import Any

import base64
import hashlib
import logging
import os

from passlib.context import CryptContext

from .constants import STATUS_OK
from .exeptions import BadRequestHTTPError, NotFoundHTTPError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

log = logging.getLogger(__name__)


class HashPass:
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if answer := pwd_context.verify(plain_password, hashed_password):
            return answer
        raise BadRequestHTTPError(message="wrong password")


def create_codes() -> dict:
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b"=").decode("utf-8")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }


async def valid_answer(response: Any) -> dict:
    if response.status != STATUS_OK:
        raise NotFoundHTTPError
    return await response.json()


def config_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )

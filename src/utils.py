from typing import Any

import base64
import hashlib
import hmac
import logging
import os

import bcrypt

from .constants import BYTES_SECRET_KEY_HASH, STATUS_OK
from .exeptions import NotFoundHTTPError

log = logging.getLogger(__name__)


class Hash:
    def get_password_hash(password: str) -> str:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(peppered_password, salt)
        return hashed.decode("utf-8")

    def verify_password(password: str, hashed_password: str) -> bool:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        return bcrypt.checkpw(peppered_password, hashed_password.encode("utf-8"))


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

from typing import Any

import base64
import hashlib
import hmac
import logging
import os
import re
from uuid import uuid4

import bcrypt
from pydantic import BaseModel

from .constants import BYTES_SECRET_KEY_HASH, CONST_10, CONST_11, STATUS_OK
from .exeptions import NotFoundHTTPError

log = logging.getLogger(__name__)


class Hash:
    @staticmethod
    def get_password_hash(password: str) -> str:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(peppered_password, salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        peppered_password = hmac.new(
            BYTES_SECRET_KEY_HASH, password.encode("utf-8"), hashlib.sha256
        ).digest()
        return bcrypt.checkpw(peppered_password, hashed_password.encode("utf-8"))


def create_codes() -> BaseModel:
    from .schemas import Codes

    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b"=").decode("utf-8")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return Codes(state=str(uuid4()), code_verifier=code_verifier, code_challenge=code_challenge)


async def valid_answer(response: Any) -> dict:
    if response.status != STATUS_OK:
        raise NotFoundHTTPError
    return await response.json()


def format_phone_number(phone_number: str) -> str:
    digits = re.sub(pattern=r"\D", repl="", string=phone_number)
    if len(digits) == CONST_11 and digits.startswith("8"):
        digits = "7" + digits[1:]
    elif len(digits) == CONST_10 and digits.startswith("9"):
        digits = "7" + digits
    return f"+{digits[0]}({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"


def config_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )

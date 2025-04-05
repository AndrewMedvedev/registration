

from typing import Any

from pydantic import BaseModel


class CustomResponse(BaseModel):
    status_code: int
    status: str = "success"
    body: Any

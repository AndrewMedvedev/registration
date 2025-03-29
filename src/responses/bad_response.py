from fastapi.responses import JSONResponse


class CustomBadResponse(JSONResponse):
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str,
    ):
        body = {
            "status_code": status_code,
            "status": "fail",
            "message": message,
            "detail": detail,
        }

        super().__init__(
            content=body,
            status_code=status_code,
        )

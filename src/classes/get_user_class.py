from fastapi.responses import JSONResponse

from src.services.orm import ORMService


class GetUser:

    def __init__(
        self,
        user_id: int,
    ) -> None:
        self.user_id = user_id

    async def get(self) -> JSONResponse:
        data = await ORMService().get_data(self.user_id)
        data_dict = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
        }
        return JSONResponse(content=data_dict)

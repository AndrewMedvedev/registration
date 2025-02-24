from fastapi.responses import JSONResponse
from src.services.orm import ORMService
from src.config import Settings as settings


class GetUser:

    def __init__(self, user_id: int, password: str) -> None:
        self.user_id = user_id
        self.password = password

    async def get(self) -> JSONResponse:
        if settings.DB_PASSWORD == self.password:
            data = await ORMService().get_data(self.user_id)
            data_dict = {
                "first_name": data.first_name,
                "last_name": data.last_name,
                "email": data.email,
            }
            return JSONResponse(content=data_dict)

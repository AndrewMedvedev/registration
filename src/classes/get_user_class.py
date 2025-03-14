from fastapi.responses import JSONResponse

from src.services.orm import ORMService


class GetUserData:

    def __init__(self) -> None:
        self.orm = ORMService()

    async def get_data(
        self,
        user_id: int,
    ) -> JSONResponse:
        data = await self.orm.get_data(user_id)
        data_dict = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
        }
        return JSONResponse(content=data_dict)

    async def get_number(
        self,
        phone_number: str,
    ) -> JSONResponse:
        return JSONResponse(
            content={"message": await self.orm.get_number(phone_number)}
        )

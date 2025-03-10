from fastapi.responses import JSONResponse

from src.services.orm import ORMService


class GetUserData:

    def __init__(
        self,
        user_id: int = None,
        phone_number: str = None
    ) -> None:
        self.user_id = user_id
        self.phone_number = phone_number
        self.orm = ORMService()

    async def get_data(self) -> JSONResponse:
        data = await self.orm.get_data(self.user_id)
        data_dict = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
        }
        return JSONResponse(content=data_dict)
    
    async def get_number(self) -> JSONResponse:
        return JSONResponse(content={"message": await self.orm.get_number(self.phone_number)})

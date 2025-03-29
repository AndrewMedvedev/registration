import logging

from fastapi import status

from src.services.orm import ORMService
from src.responses import CustomResponse

log = logging.getLogger(__name__)


class GetUserData:

    def __init__(self) -> None:
        self.orm = ORMService()

    async def get_data(
        self,
        user_id: int,
    ) -> CustomResponse:
        data = await self.orm.get_data(user_id)
        data_dict = {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "email": data.email,
        }
        log.debug(data_dict)
        return CustomResponse(
            body=data_dict,
            status_code=status.HTTP_200_OK,
        )

    async def get_number(
        self,
        phone_number: str,
    ) -> CustomResponse:
        answer = await self.orm.get_number(phone_number)
        log.debug(answer)
        return CustomResponse(
            body=answer,
            status_code=status.HTTP_200_OK,
        )

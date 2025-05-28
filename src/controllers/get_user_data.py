from uuid import UUID

from ..baseclasses import BaseControl
from ..database.crud import SQLAuthorization


class GetUserDataControl(BaseControl):
    def __init__(self) -> None:
        self.sql_authorization = SQLAuthorization()

    async def get_data(self, user_id: UUID) -> dict:
        data_user = await self.sql_authorization.get_data(user_id=user_id)
        self.logger.warning(data_user)
        return data_user

    async def get_number(self, phone_number: str) -> str:
        user_id = await self.sql_authorization.get_number(phone_number=phone_number)
        self.logger.warning(user_id)
        return user_id

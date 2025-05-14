from uuid import UUID

from ..database.crud import SQLAuthorization


class GetUserDataControl:
    def __init__(self) -> None:
        self.sql_authorization = SQLAuthorization()

    async def get_data(self, user_id: UUID) -> dict:
        return await self.sql_authorization.get_data(user_id=user_id)

    async def get_number(self, phone_number: str) -> str:
        return await self.sql_authorization.get_number(phone_number=phone_number)

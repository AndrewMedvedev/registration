from src.classes.jwt_classes import JWTCreate
from src.services.orm import ORMService
from src.config import Settings as settings
import aiohttp


class VK:

    def __init__(
        self,
        params: dict = None,
        data: dict = None,
        email: str = None,
        user_model=None,
    ) -> None:
        self._params = params
        self._data = data
        self._email = email
        self._user_model = user_model

    async def get_data_user(self) -> dict:
        if self._params is not None:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    settings.VK_TOKEN_URL, params=self._params, ssl=False
                ) as data:
                    user_data = await data.json()
                    return user_data

    async def data_add(self) -> None:
        if self._user_model is not None:
            await ORMService().add_user(self._user_model)

    async def data_get(self) -> bool:
        if self._email is not None:
            stmt = await ORMService().get_user_email_vk(self._email)
            if stmt.email == self._email:
                return True
            else:
                return False

    async def create_tokens(self) -> dict:
        if self._data is not None:
            access = await JWTCreate(self._data).create_access()
            refresh = await JWTCreate(self._data).create_refresh()
            tokens = {"access": access, "refresh": refresh}
            return tokens

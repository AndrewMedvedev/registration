from aiohttp import ClientSession

from config import settings

from .baseclasses import BaseAPI
from .utils import valid_answer


class VKApi(BaseAPI):
    async def get_token(self, params: dict) -> dict:
        async with (
            ClientSession() as session,
            session.post(url=settings.VK_TOKEN_URL, json=params, ssl=False) as data,
        ):
            self.logger.warning(data)
            return await valid_answer(response=data)

    async def get_data(self, params: dict) -> dict:
        async with (
            ClientSession() as session,
            session.post(url=settings.VK_API_URL, json=params, ssl=False) as data,
        ):
            self.logger.warning(data)
            return (await valid_answer(response=data))["user"]


class YandexApi(BaseAPI):
    async def get_token(self, params: dict) -> dict:
        async with (
            ClientSession() as session,
            session.post(url=settings.YANDEX_TOKEN_URL, data=params, ssl=False) as data,
        ):
            self.logger.warning(data)
            return await valid_answer(response=data)

    async def get_data(self, params: dict) -> dict:
        async with (
            ClientSession() as session,
            session.get(url=settings.YANDEX_API_URL, params=params, ssl=False) as data,
        ):
            self.logger.warning(data)
            return await valid_answer(response=data)

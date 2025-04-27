from aiohttp import ClientSession

from config import Settings

from .utils import valid_answer


class VKApi:
    def __init__(self):
        self.clientsession = ClientSession

    async def get_token(self, params: dict) -> dict:
        async with (
            self.clientsession() as session,
            session.post(url=Settings.VK_TOKEN_URL, json=params, ssl=False) as data,
        ):
            return await valid_answer(response=data)

    async def get_data(self, params: dict) -> dict:
        async with (
            self.clientsession() as session,
            session.post(url=Settings.VK_API_URL, json=params, ssl=False) as data,
        ):
            return (await valid_answer(response=data))["user"]


class YandexApi:
    def __init__(self):
        self.clientsession = ClientSession

    async def get_token(self, params: dict) -> dict:
        async with (
            self.clientsession() as session,
            session.post(url=Settings.YANDEX_TOKEN_URL, data=params, ssl=False) as data,
        ):
            return await valid_answer(response=data)

    async def get_data(self, params: dict) -> dict:
        async with (
            self.clientsession() as session,
            session.get(url=Settings.YANDEX_API_URL, params=params, ssl=False) as data,
        ):
            return await valid_answer(response=data)

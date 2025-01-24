import aiohttp
from passlib.context import CryptContext
from src.config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPass:

    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


async def get_data_user_vk(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            Settings.VK_TOKEN_URL, json=params, ssl=False
        ) as data:
            user_data = await data.json()
            return user_data


async def get_token_user_yandex(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            Settings.YANDEX_TOKEN_URL, data=params, ssl=False
        ) as data:
            user_data = await data.json()
            return user_data
        

async def get_data_user_yandex(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            Settings.YANDEX_API_URL, params=params, ssl=False
        ) as data:
            user_data = await data.json()
            return user_data


async def get_token_user_mail_ru(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            Settings.MAIL_RU_TOKEN_URL, params=params, ssl=False
        ) as data:
            user_data = await data.json()
            return user_data


async def get_data_user_mail_ru(params: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            Settings.MAIL_RU_API_URL, params=params, ssl=False
        ) as data:
            user_data = await data.json()
            return user_data

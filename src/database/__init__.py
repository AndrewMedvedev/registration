__all__ = (
    "HashPass",
    "get_token_user_vk",
    "get_data_user_vk",
    "get_token_user_mail_ru",
    "get_data_user_mail_ru",
    "get_token_user_yandex",
    "get_data_user_yandex",
)

from src.database.controls import (HashPass, get_data_user_mail_ru,
                                   get_data_user_vk, get_data_user_yandex,
                                   get_token_user_mail_ru, get_token_user_vk,
                                   get_token_user_yandex)


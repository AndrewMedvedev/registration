__all__ = [
    "AuthorizationControl",
    "GetUserDataControl",
    "RegistrationControl",
    "VKControl",
    "YandexControl",
]

from .authorization import AuthorizationControl, RegistrationControl
from .get_user_data import GetUserDataControl
from .vk import VKControl
from .yandex import YandexControl

__all__ = [
    "AuthorizationControl",
    "GetUserDataControl",
    "RegistrationControl",
    "ReplacePasswordControl",
    "VKControl",
    "YandexControl",
]

from .authorization import AuthorizationControl, RegistrationControl, ReplacePasswordControl
from .get_user_data import GetUserDataControl
from .vk import VKControl
from .yandex import YandexControl

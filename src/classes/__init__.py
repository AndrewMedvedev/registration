__all__ = (
    "Authorization",
    "JWTCreate",
    "ValidateJWT",
    # "MailRu",
    "VK",
    "Yandex",
    "GetUserData",
)

from .authorization_class import Authorization
from .get_user_class import GetUserData
from .jwt_classes import JWTCreate, ValidateJWT

# from src.classes.mail_ru_class import MailRu
from .vk_class import VK
from .yandex_class import Yandex

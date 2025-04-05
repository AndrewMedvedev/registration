__all__ = (
    "DictGetDataMailRu",
    "DictGetDataTokenMailRu",
    "DictGetDataTokenVK",
    "DictGetDataTokenYandex",
    "DictGetDataVK",
    "DictGetDataYandex",
    "DictLinkMailRu",
    "DictLinkVK",
    "DictLinkYandex",
    "GetUserEmail",
    "GetUserPhoneNumber",
    "RegistrationVK",
    "RegistrationYandex",
    "UserModel",
)

from src.database.schemas.auth_schemas import GetUserEmail, GetUserPhoneNumber, UserModel
from src.database.schemas.mail_ru_schemas import DictGetDataMailRu, DictGetDataTokenMailRu, DictLinkMailRu
from src.database.schemas.vk_schemas import DictGetDataTokenVK, DictGetDataVK, DictLinkVK, RegistrationVK
from src.database.schemas.yandex_schemas import DictGetDataTokenYandex, DictGetDataYandex, DictLinkYandex, RegistrationYandex

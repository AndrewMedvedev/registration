__all__ = (
    "UserModel",
    "GetUserEmail",
    "GetUserPhoneNumber",
    "DictGetDataMailRu",
    "DictGetDataTokenMailRu",
    "DictLinkMailRu",
    "DictGetDataVK",
    "DictGetDataTokenVK",
    "DictLinkVK",
    "DictGetDataYandex",
    "DictGetDataTokenYandex",
    "DictLinkYandex",
)

from src.database.schemas.auth_schemas import UserModel, GetUserEmail, GetUserPhoneNumber
from src.database.schemas.mail_ru_schemas import DictGetDataMailRu, DictGetDataTokenMailRu, DictLinkMailRu
from src.database.schemas.vk_schemas import DictGetDataVK, DictGetDataTokenVK, DictLinkVK
from src.database.schemas.yandex_schemas import DictGetDataYandex, DictGetDataTokenYandex, DictLinkYandex
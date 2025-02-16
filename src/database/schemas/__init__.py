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

from src.database.schemas.auth_schemas import (GetUserEmail,
                                               GetUserPhoneNumber, UserModel)
from src.database.schemas.mail_ru_schemas import (DictGetDataMailRu,
                                                  DictGetDataTokenMailRu,
                                                  DictLinkMailRu)
from src.database.schemas.vk_schemas import (DictGetDataTokenVK, DictGetDataVK,
                                             DictLinkVK)
from src.database.schemas.yandex_schemas import (DictGetDataTokenYandex,
                                                 DictGetDataYandex,
                                                 DictLinkYandex)

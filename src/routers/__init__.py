__all__ = (
    "router_authorization",
    "router_vk",
    "router_yandex",
    "router_mail_ru",
    "router_validate_jwt",
)


from src.routers.authorization import router_authorization
from src.routers.mail_ru import router_mail_ru
from src.routers.validate_jwt import router_validate_jwt
from src.routers.vk import router_vk
from src.routers.yandex import router_yandex

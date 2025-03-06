__all__ = (
    "CRUDBase",
    "AuthorizationBase",
    "ReUseBase",
    "OtherAuthorizationsBase",
)

from src.interfaces.authorization_interface import AuthorizationBase
from src.interfaces.crud_interface import CRUDBase
from src.interfaces.other_authorizations_interface import OtherAuthorizationsBase
from src.interfaces.reuse_interface import ReUseBase

__all__ = (
    "AuthorizationsBase",
    "BasicAuthorizationBase",
    "CRUDBase",
)

from .basic_authorization_interface import BasicAuthorizationBase
from .crud_interface import CRUDBase
from .other_auth_interface import AuthorizationsBase

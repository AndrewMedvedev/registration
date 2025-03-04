from abc import ABC, abstractmethod


class CRUDBase(ABC):

    @abstractmethod
    async def add_user(
        self,
        user,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_user_email(
        self,
        email: str,
        hash_password: str,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_user_phone_number(
        self,
        phone_number: str,
        hash_password: str,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_data(
        self,
        user_id: int,
    ) -> dict:
        raise NotImplementedError

from abc import ABCMeta, abstractmethod
from typing import Optional

from src.db.models.user_model import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_sub_id(self, sub_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        pass

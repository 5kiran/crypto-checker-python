import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional

from src.db.models.wallet_model import Wallet


class IWalletRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create_wallet(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    async def get_wallets(self, user_id: uuid.UUID) -> list[Wallet]:
        pass

    @abstractmethod
    async def get_wallet(
        self, wallet_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Wallet]:
        pass

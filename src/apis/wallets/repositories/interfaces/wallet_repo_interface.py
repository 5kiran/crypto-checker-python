from abc import ABCMeta, abstractmethod

from src.db.models.wallet_model import Wallet


class IWalletRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create_wallet(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    async def get_wallets(self, user_id: str) -> list[Wallet]:
        pass

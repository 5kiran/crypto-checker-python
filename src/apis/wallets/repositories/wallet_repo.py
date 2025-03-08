from dependency_injector.wiring import Provide
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.apis.wallets.repositories.interfaces.wallet_repo_interface import (
    IWalletRepository,
)
from src.db.models.wallet_model import Wallet


class WalletRepository(IWalletRepository):
    def __init__(self, db: Session = Depends(Provide["db_session"])):
        self.db = db

    async def create_wallet(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)

        return wallet

    async def get_wallets(self, user_id: str) -> list[Wallet]:
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        wallets = self.db.execute(stmt).scalars().all()

        return list(wallets)

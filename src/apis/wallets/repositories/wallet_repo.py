import uuid
from typing import Optional

from dependency_injector.wiring import Provide
from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from src.apis.wallets.repositories.interfaces.wallet_repo_interface import (
    IWalletRepository,
)
from src.db.models.joined_mission_model import JoinedMission
from src.db.models.mission_model import Mission
from src.db.models.wallet_model import Wallet


class WalletRepository(IWalletRepository):
    def __init__(self, db: Session = Depends(Provide["db_session"])):
        self.db = db

    async def create_wallet(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)

        return wallet

    async def get_wallets(self, user_id: uuid.UUID) -> list[Wallet]:
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        wallets = self.db.execute(stmt).scalars().all()

        return list(wallets)

    async def get_wallet(
        self, wallet_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Wallet]:
        stmt = (
            select(Wallet)
            .options(
                joinedload(Wallet.joined_missions).joinedload(JoinedMission.mission)
            )
            .where(Wallet.id == wallet_id and Wallet.user_id == user_id)
        )

        wallet = self.db.execute(stmt).scalars().first()
        return wallet

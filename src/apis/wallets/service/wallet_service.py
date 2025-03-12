import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.apis.wallets.dto.request.create_wallet_request import CreateWalletRequest
from src.apis.wallets.repositories.interfaces.wallet_repo_interface import (
    IWalletRepository,
)
from src.db.models.user_model import User
from src.db.models.wallet_model import Wallet


class WalletService:
    @inject
    def __init__(
        self,
        wallet_repository: IWalletRepository,
        db: Session = Depends(Provide["db_session"]),
    ):
        self.db = db
        self.wallet_repository = wallet_repository

    async def create_wallet(self, body: CreateWalletRequest, user: User) -> Wallet:
        _wallet = Wallet(
            name=body.name, type=body.type, address=body.address, user_id=user.id
        )

        wallet = await self.wallet_repository.create_wallet(_wallet)

        self.db.commit()
        return wallet

    async def get_wallets(self, user: User) -> list[Wallet]:
        wallets = await self.wallet_repository.get_wallets(user.id)

        return wallets

    async def get_wallet(self, wallet_id: uuid.UUID, user: User) -> Wallet:
        wallet = await self.wallet_repository.get_wallet(
            wallet_id=wallet_id, user_id=user.id
        )

        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        return wallet

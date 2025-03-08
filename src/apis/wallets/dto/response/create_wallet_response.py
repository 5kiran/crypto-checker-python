import uuid

from pydantic import BaseModel

from src.db.models.wallet_model import WalletType


class CreateWalletResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: WalletType
    address: str
    user_id: uuid.UUID

    class Config:
        from_attributes = True

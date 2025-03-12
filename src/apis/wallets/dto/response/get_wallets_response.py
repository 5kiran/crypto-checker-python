import uuid

from pydantic import BaseModel

from src.db.models.wallet_model import WalletType


class GetWalletsResponse(BaseModel):
    id: uuid.UUID
    name: str
    type: WalletType
    address: str

    class Config:
        from_attributes = True

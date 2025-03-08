from pydantic import BaseModel

from src.db.models.wallet_model import WalletType


class CreateWalletRequest(BaseModel):
    name: str
    type: WalletType
    address: str

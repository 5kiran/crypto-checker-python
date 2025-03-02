import enum
import uuid
from typing import Optional

from sqlalchemy import String, text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.database import Base
from src.db.models.user_model import User


class WalletType(enum.Enum):
    EVM = "EVM"
    SOL = "SOL"
    SUI = "SUI"


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="지갑 이름"
    )
    address: Mapped[str] = mapped_column(String, nullable=False, comment="지갑 주소")

    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="유저 id"
    )
    user: Mapped["User"] = relationship("User", back_populates="wallets")

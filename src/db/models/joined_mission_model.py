import uuid
from dataclasses import dataclass

from sqlalchemy import Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


@dataclass
class JoinedMission(Base):
    __tablename__ = "joined_mission"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    mission_id: Mapped[str] = mapped_column(
        ForeignKey("mission.id", ondelete="CASCADE"),
        nullable=False,
        comment="미션 id",
    )
    mission: Mapped["Mission"] = relationship(
        "Mission", back_populates="joined_missions"
    )

    wallet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("wallet.id", ondelete="CASCADE"),
        nullable=False,
        comment="지갑 id",
    )
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="joined_missions")

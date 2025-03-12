import enum
import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Uuid, text, String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class Layer(enum.Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


@dataclass
class Project(Base):
    __tablename__ = "project"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String, nullable=False, comment="체인 이름")
    layer: Mapped[Layer] = mapped_column(
        Enum(Layer), nullable=False, default=Layer.L1, comment="L1,L2,L3"
    )
    image: Mapped[str] = mapped_column(String, nullable=False, comment="체인 이미지")
    home_page: Mapped[str] = mapped_column(String, nullable=False, comment="홈페이지")
    discord: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="디스코드 주소"
    )
    twitter: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="트위터 주소"
    )
    twitter_handle: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="트위터 핸들"
    )
    contract: Mapped[str] = mapped_column(
        String, nullable=True, unique=True, comment="체인 계약 주소"
    )
    test_contract: Mapped[bool] = mapped_column(
        String, nullable=True, unique=True, comment="테스트 계약 여부"
    )

    missions: Mapped[list["Mission"]] = relationship(
        "Mission",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="noload",
    )

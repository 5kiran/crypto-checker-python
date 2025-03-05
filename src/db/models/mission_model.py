import datetime
import enum
import uuid
from typing import Optional

from sqlalchemy import Uuid, text, Enum, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class MissionType(enum.Enum):
    WAIT_LIST = "WAIT_LIST"
    WHITE_LIST = "WHITE_LIST"
    VAULT = "VAULT"
    QUEST = "QUEST"


class Mission(Base):
    __tablename__ = "mission"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    type: Mapped[MissionType] = mapped_column(
        Enum(MissionType), nullable=False, comment="미션 종류"
    )
    title: Mapped[str] = mapped_column(String, nullable=False, comment="제목")
    url: Mapped[str] = mapped_column(String, nullable=False, comment="미션 페이지 URL")
    start_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="참여 시작 시간"
    )
    end_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, comment="참여 종료 시간"
    )
    draw_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, nullable=True, comment="추첨 시간"
    )
    reward_date: Mapped[Optional[datetime.date]] = mapped_column(
        Date, nullable=True, comment="보상 시간"
    )

    project_id: Mapped[str] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False,
        comment="프로젝트 id",
    )
    project: Mapped["Project"] = relationship("Project", back_populates="missions")

    joined_missions: Mapped[list["JoinedMission"]] = relationship(
        "JoinedMission", back_populates="mission", cascade="all, delete-orphan"
    )

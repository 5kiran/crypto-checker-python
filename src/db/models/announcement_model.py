import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class Announcement(Base):
    __tablename__ = "announcement"

    sequence_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="시퀀스 번호"
    )
    title: Mapped[str] = mapped_column(String, nullable=False, comment="제목")
    content: Mapped[str] = mapped_column(String, nullable=False, comment="본문")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default="now()"
    )

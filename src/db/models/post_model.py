import datetime
import uuid
from dataclasses import dataclass

from sqlalchemy import String, DateTime, ForeignKey, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


@dataclass
class Post(Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    title: Mapped[str] = mapped_column(String, nullable=False, comment="제목")
    content: Mapped[str] = mapped_column(String, nullable=False, comment="본문")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, comment="업데이트 시간"
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        comment="유저 id",
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
        lazy="noload",
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="noload",
    )

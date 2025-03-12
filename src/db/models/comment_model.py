import uuid
from dataclasses import dataclass

from sqlalchemy import Uuid, text, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.db.database import Base


@dataclass
class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    content: Mapped[str] = mapped_column(String, nullable=False, comment="본문")

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, comment="유저 id"
    )
    user: Mapped["User"] = relationship("User", back_populates="comments")

    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
        comment="게시글 id",
    )
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
        lazy="noload",
    )

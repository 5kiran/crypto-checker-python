import datetime
import enum
import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import String, Enum, DateTime, text, Uuid, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.database import Base


class UserRole(enum.Enum):
    SUBSCRIBER = "SUBSCRIBER"
    CERTIFICATE = "CERTIFICATE"
    TEMP = "TEMP"
    ADMIN = "ADMIN"


@dataclass
class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    sub_id: Mapped[str] = mapped_column(String, nullable=False, comment="GOOGLE_SUB_ID")
    nickname: Mapped[str] = mapped_column(String, nullable=False, comment="닉네임")
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True, comment="이름")
    phone_number: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="휴대폰번호"
    )
    email: Mapped[str] = mapped_column(String, nullable=False, comment="이메일")
    profile_image: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="프로필 이미지"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.TEMP, nullable=False, comment="유저 권한"
    )
    reward_notification: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="리워드 알림 설정"
    )
    refresh_token: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="리프레쉬 토큰"
    )
    signed_at: Mapped[datetime] = mapped_column(
        DateTime, default="now()", nullable=False, comment="가입 시간"
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="업데이트 시간"
    )
    withdrawal_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, comment="탈퇴 시간"
    )

    wallets: Mapped[list["Wallet"]] = relationship(
        "Wallet", back_populates="user", cascade="all, delete-orphan"
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan"
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    joined_missions: Mapped[list["JoinedMission"]] = relationship(
        "JoinedMission", back_populates="user", cascade="all, delete-orphan"
    )

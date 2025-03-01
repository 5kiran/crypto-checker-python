import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Enum, DateTime, text, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.db.database import Base


class UserRole(enum.Enum):
    SUBSCRIBER = "SUBSCRIBER"
    CERTIFICATE = "CERTIFICATE"
    TEMP = "TEMP"


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    nickname: Mapped[str] = mapped_column(String, nullable=False, comment="닉네임")
    name: Mapped[str | None] = mapped_column(String, nullable=True, comment="이름")
    phone_number: Mapped[str | None] = mapped_column(
        String, nullable=True, comment="휴대폰번호"
    )
    email: Mapped[str] = mapped_column(String, nullable=False, comment="이메일")
    profile_image: Mapped[str | None] = mapped_column(
        String, nullable=True, comment="프로필 이미지"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.TEMP, nullable=False, comment="유저 권한"
    )
    refresh_token: Mapped[str | None] = mapped_column(
        String, nullable=True, comment="리프레쉬 토큰"
    )
    signed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False, comment="가입 시간"
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="업데이트 시간"
    )
    withdrawal_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="탈퇴 시간"
    )

    wallets: Mapped["Wallet"] = relationship(
        "Wallet", back_populates="user", cascade="all, delete-orphan"
    )


# enum UserRole {
#   SUBSCRIBER
#   CERTIFICATE
#   TEMP
# }

# model User {
#   id String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))// 로그인 ID
#   nickname String @db.Text // 닉네임
#   name String? @db.Text // 실제 이름
#   phoneNumber String? @db.Text @map("phone_number") // 휴대폰 번호
#   email String @db.Text @unique // 이메일
#   image String? @db.Text @map("image") // 프로필 이미지
#   role UserRole @default(TEMP) // 유저 롤
#   refreshToken String? @db.Text @map("refresh_token")
#   signedAt DateTime @db.Timestamp()  @default(now()) @map("signed_at") // 가입일
#   updatedAt DateTime? @db.Timestamp() @updatedAt @map("updated_at") // 업데이트 시간
#   withdrawalAt DateTime? @db.Timestamp() @map("withdrawal_at") // 탈퇴일

#   wallets Wallet[]
#   missions JoinedMission[]
# }

# enum WalletType {
#   EVM
#   SOL
#   SUI
# }

# model Wallet {
#   id String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))
#   name String @db.Text
#   address String @db.Text
#   detection Boolean @db.Boolean @default(false)
#   connectedAt DateTime @db.Timestamp() @map("connected_at")
#   recentConnectedAt DateTime @db.Timestamp() @map("recent_connected_at")

#   user User? @relation(fields: [userId], references: [id], onDelete: Cascade)
#   userId String? @db.Uuid @map("user_id")

#   joinedMission JoinedMission[]
# }

# model Chain {
#   id String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))
#   name String @db.Text
#   web String? @db.Text
#   discord String? @db.Text
#   twitter String? @db.Text
#   twitterHandle String? @db.Text
#   image String @db.Text
#   contract String? @db.Text
#   testContract String? @db.Text @map("test_contract")

#   projects Project[]
# }

# model Project {
#   id String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))
#   name String @db.Text
#   image String @db.Text
#   web String? @db.Text
#   discord String? @db.Text
#   twitter String? @db.Text
#   twitterHandle String? @db.Text

#   chain Chain? @relation(fields: [chainId], references: [id], onDelete: SetNull)
#   chainId String? @db.Uuid @map("chain_id")
# }

# enum MissionType {
#   WAIT_LIST
#   WHITE_LIST
#   QUEST
#   VAULT
# }

# model Mission {
#   id String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))
#   type MissionType
#   title String @db.Text
#   missionPage String @db.Text @map("mission_page")
#   startDate DateTime @db.Timestamp() @map("start_date")
#   endDate DateTime @db.Timestamp() @map("end_date")
#   claimDate DateTime? @db.Date @map("claim_date")

#   joinedMission JoinedMission[]
# }

# model JoinedMission {
#   id        String @db.Uuid @id @default(dbgenerated("gen_random_uuid()"))
#   userId    String @db.Uuid @map("user_id")
#   missionId String @db.Uuid @map("mission_id")
#   walletId  String @db.Uuid @map("wallet_id")
#   createdAt DateTime @db.Date @default(now())

#   user    User    @relation(fields: [userId], references: [id], onDelete: Cascade)
#   mission Mission @relation(fields: [missionId], references: [id], onDelete: Cascade)
#   wallet  Wallet  @relation(fields: [walletId], references: [id], onDelete: Cascade)
# }

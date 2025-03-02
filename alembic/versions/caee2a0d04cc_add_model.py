"""Add Model

Revision ID: caee2a0d04cc
Revises:
Create Date: 2025-03-01 20:56:22.587504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "caee2a0d04cc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("nickname", sa.String(), nullable=False, comment="닉네임"),
        sa.Column("name", sa.String(), nullable=True, comment="이름"),
        sa.Column("phone_number", sa.String(), nullable=True, comment="휴대폰번호"),
        sa.Column("email", sa.String(), nullable=False, comment="이메일"),
        sa.Column("profile_image", sa.String(), nullable=True, comment="프로필 이미지"),
        sa.Column(
            "role",
            sa.Enum("SUBSCRIBER", "CERTIFICATE", "TEMP", name="userrole"),
            nullable=False,
            comment="유저 권한",
        ),
        sa.Column("refresh_token", sa.String(), nullable=True, comment="리프레쉬 토큰"),
        sa.Column("signed_at", sa.DateTime(), nullable=False, comment="가입 시간"),
        sa.Column("updated_at", sa.DateTime(), nullable=True, comment="업데이트 시간"),
        sa.Column("withdrawal_at", sa.DateTime(), nullable=True, comment="탈퇴 시간"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "wallet",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("wallet")
    op.drop_table("user")
    # ### end Alembic commands ###

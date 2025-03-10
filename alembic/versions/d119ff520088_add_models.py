"""Add Models

Revision ID: d119ff520088
Revises: 48f8a04dea68
Create Date: 2025-03-05 15:04:38.177504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d119ff520088"
down_revision: Union[str, None] = "48f8a04dea68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "joined_mission",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("mission_id", sa.Uuid(), nullable=False, comment="미션 id"),
        sa.Column("user_id", sa.Uuid(), nullable=False, comment="미션 id"),
        sa.ForeignKeyConstraint(["mission_id"], ["mission.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("joined_mission")
    # ### end Alembic commands ###

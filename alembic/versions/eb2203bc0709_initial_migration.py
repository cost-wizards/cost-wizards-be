"""initial migration

Revision ID: eb2203bc0709
Revises: 
Create Date: 2024-04-06 02:20:09.427354

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "eb2203bc0709"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass

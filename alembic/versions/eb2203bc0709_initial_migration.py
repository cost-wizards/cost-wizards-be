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
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("access_key", sa.String(), nullable=True),
        sa.Column("secret_key", sa.String(), nullable=True),
        sa.Column("region", sa.String(), nullable=True),
        sa.Column("session_key", sa.String(), nullable=True),
        sa.Column("has_account_setup", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "instance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("instance_id", sa.String(), nullable=True),
        sa.Column("instance_type", sa.String(), nullable=True),
        sa.Column("vcpu", sa.String(), nullable=True),
        sa.Column("instance_memory", sa.String(), nullable=True),
        sa.Column("network_performance", sa.String(), nullable=True),
        sa.Column("on_demand_price", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "instance_stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instance_id", sa.String()),
        sa.Column("timestamp", sa.DateTime()),
        sa.Column("avg_cpu_usage", sa.Float(), nullable=True),
        sa.Column("max_cpu_usage", sa.Float(), nullable=True),
        sa.Column("min_cpu_usage", sa.Float(), nullable=True),
        sa.Column("avg_mem_usage", sa.Float(), nullable=True),
        sa.Column("max_mem_usage", sa.Float(), nullable=True),
        sa.Column("min_mem_usage", sa.Float(), nullable=True),
        sa.Column("avg_network_in", sa.Float(), nullable=True),
        sa.Column("max_network_in", sa.Float(), nullable=True),
        sa.Column("min_network_in", sa.Float(), nullable=True),
        sa.Column("avg_network_out", sa.Float(), nullable=True),
        sa.Column("max_network_out", sa.Float(), nullable=True),
        sa.Column("min_network_out", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "recommendation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sug_1_instance_type", sa.String(), nullable=True),
        sa.Column("sug_1_reason", sa.String(), nullable=True),
        sa.Column("sug_1_cost_per_hour", sa.String(), nullable=True),
        sa.Column("sug_1_diff_cost_per_hour", sa.String(), nullable=True),
        sa.Column("sug_2_instance_type", sa.String(), nullable=True),
        sa.Column("sug_2_reason", sa.String(), nullable=True),
        sa.Column("sug_2_cost_per_hour", sa.String(), nullable=True),
        sa.Column("sug_2_diff_cost_per_hour", sa.String(), nullable=True),
        sa.Column("instance_id", sa.Integer(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["instance_id"], ["instance.id"]),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    pass

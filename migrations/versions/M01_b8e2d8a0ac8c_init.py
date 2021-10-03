"""init

Revision ID: b8e2d8a0ac8c
Revises: 
Create Date: 2021-10-02 17:43:25.323978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b8e2d8a0ac8c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
    )


def downgrade():
    op.drop_table("users")

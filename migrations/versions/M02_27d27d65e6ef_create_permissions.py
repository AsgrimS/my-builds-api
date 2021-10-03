"""create permissions

Revision ID: 27d27d65e6ef
Revises: 59f0ee41c5a2
Create Date: 2021-10-03 15:50:57.901311

"""
from alembic import op
import sqlalchemy as sa

from app.models.users import Permission
from app.config import Permissions
from app.database import get_db

# revision identifiers, used by Alembic.
revision = "27d27d65e6ef"
down_revision = "59f0ee41c5a2"
branch_labels = None
depends_on = None


def upgrade():
    db = next(get_db())
    admin_permissions = Permission(name=Permissions.admin_permission)
    db.add(admin_permissions)
    db.commit()


def downgrade():
    db = next(get_db())
    db.query(Permission).delete()
    db.commit()

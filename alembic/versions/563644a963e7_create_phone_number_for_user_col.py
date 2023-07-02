"""create phone number for user col

Revision ID: 563644a963e7
Revises: 
Create Date: 2023-07-02 11:18:46.590502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '563644a963e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')

"""create adress table

Revision ID: c596b5fdda40
Revises: 563644a963e7
Create Date: 2023-07-02 11:32:13.052071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c596b5fdda40'
down_revision = '563644a963e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(length=100),nullable=False),
                    sa.Column('address2', sa.String(length=100), nullable=False),
                    sa.Column('city', sa.String(length=100), nullable=False),
                    sa.Column('state', sa.String(length=100), nullable=False),
                    sa.Column('country', sa.String(length=100), nullable=False),
                    sa.Column('postalcode', sa.String(length=100), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('address')
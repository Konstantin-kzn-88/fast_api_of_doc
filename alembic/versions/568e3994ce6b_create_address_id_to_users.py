"""create address_id to users

Revision ID: 568e3994ce6b
Revises: c596b5fdda40
Create Date: 2023-07-02 11:37:52.706598

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '568e3994ce6b'
down_revision = 'c596b5fdda40'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk',
                          source_table='users',
                          referent_table='address',
                          local_cols=['address_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users', type_='foreignkey')
    op.drop_column('users', 'address_id')

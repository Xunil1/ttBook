"""Add to User table token field

Revision ID: 64ee13655d9d
Revises: b3c00d6bfbb0
Create Date: 2024-04-11 13:23:26.159308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64ee13655d9d'
down_revision = 'b3c00d6bfbb0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'token')
    # ### end Alembic commands ###
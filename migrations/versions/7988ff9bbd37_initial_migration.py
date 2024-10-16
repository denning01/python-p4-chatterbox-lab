"""Initial migration

Revision ID: 7988ff9bbd37
Revises: 48875a91c67e
Create Date: 2024-10-13 21:53:46.563057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7988ff9bbd37'
down_revision = '48875a91c67e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('messages')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('message')
    # ### end Alembic commands ###

"""Added token table

Revision ID: ea699c4fdb96
Revises: 2a6d3c0612d3
Create Date: 2020-05-05 21:32:30.821740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea699c4fdb96'
down_revision = '2a6d3c0612d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.Text(), nullable=False),
    sa.Column('create_date', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_token'))
    )
    op.create_index(op.f('ix_token_token'), 'token', ['token'], unique=False)
    op.create_index(op.f('ix_token_user_id'), 'token', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_user_id'), table_name='token')
    op.drop_index(op.f('ix_token_token'), table_name='token')
    op.drop_table('token')
    # ### end Alembic commands ###
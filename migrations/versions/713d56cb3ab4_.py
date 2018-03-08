"""empty message

Revision ID: 713d56cb3ab4
Revises: fd16e58f4c40
Create Date: 2018-02-04 02:47:37.513140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '713d56cb3ab4'
down_revision = 'fd16e58f4c40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('emotions', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('thoughts', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'thoughts')
    op.drop_column('user', 'emotions')
    # ### end Alembic commands ###

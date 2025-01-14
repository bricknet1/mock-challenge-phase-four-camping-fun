"""added validation

Revision ID: ebe4da87d2af
Revises: ba699e08b095
Create Date: 2023-03-17 11:44:41.585257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe4da87d2af'
down_revision = 'ba699e08b095'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campers', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('campers', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###

"""Add complaint

Revision ID: 6d0715a2956d
Revises: b18959076ca3
Create Date: 2023-07-04 23:33:50.041361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d0715a2956d'
down_revision = 'b18959076ca3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reason', sa.Enum('first', 'second', 'third', name='complaintenum'), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaints_id'), 'complaints', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_complaints_id'), table_name='complaints')
    op.drop_table('complaints')
    # ### end Alembic commands ###

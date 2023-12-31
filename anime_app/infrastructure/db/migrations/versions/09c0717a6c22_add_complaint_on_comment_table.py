"""Add Complaint on Comment Table

Revision ID: 09c0717a6c22
Revises: 44852684406a
Create Date: 2023-07-21 01:37:24.137089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c0717a6c22'
down_revision = '44852684406a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('complaint_comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaint_comment_id'), 'complaint_comment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_complaint_comment_id'), table_name='complaint_comment')
    op.drop_table('complaint_comment')
    # ### end Alembic commands ###

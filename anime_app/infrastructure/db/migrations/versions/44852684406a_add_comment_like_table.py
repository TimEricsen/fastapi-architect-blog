"""Add Comment Like Table

Revision ID: 44852684406a
Revises: 6d773497ae61
Create Date: 2023-07-21 00:19:42.835254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44852684406a'
down_revision = '6d773497ae61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment_likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('user', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user'], ['users.username'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('comment_id', 'user', name='comment_user_uc')
    )
    op.create_index(op.f('ix_comment_likes_id'), 'comment_likes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_likes_id'), table_name='comment_likes')
    op.drop_table('comment_likes')
    # ### end Alembic commands ###

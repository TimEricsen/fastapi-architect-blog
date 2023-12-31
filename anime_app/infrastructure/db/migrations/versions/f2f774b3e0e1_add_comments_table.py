"""Add Comments Table

Revision ID: f2f774b3e0e1
Revises: 12d03a383fba
Create Date: 2023-07-10 00:18:14.411222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2f774b3e0e1'
down_revision = '12d03a383fba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('author', sa.String(), server_default='Deleted Account!', nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('time_posted', sa.DateTime(), nullable=True),
    sa.Column('answer_to', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['answer_to'], ['comments.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['author'], ['users.username'], ondelete='SET DEFAULT'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###

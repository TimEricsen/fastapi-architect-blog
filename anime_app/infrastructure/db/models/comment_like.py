from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base
from anime_app.core.models import dto


class CommentLike(Base):
    __tablename__ = 'comment_likes'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id', ondelete='cascade'))
    user = Column(String, ForeignKey('users.username', ondelete='cascade'))

    comment = relationship('Comment', back_populates='likes')
    username = relationship('User', back_populates='comment_likes')

    __table_args__ = (UniqueConstraint('comment_id', 'user', name='comment_user_uc'),)

    def to_dto(self) -> dto.CommentLikeMain:
        return dto.CommentLikeMain(
            comment_id=self.comment_id,
            user=self.user
        )

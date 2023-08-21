from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base
from anime_app.core.models import dto


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='cascade'))
    user = Column(String, ForeignKey('users.username', ondelete='cascade'))

    post = relationship('Post', back_populates='likes')
    username = relationship('User', back_populates='likes')

    __table_args__ = (UniqueConstraint('post_id', 'user', name='post_user_uc'),)

    def to_dto(self) -> dto.MainLike:
        return dto.MainLike(
            post_id=self.post_id,
            username=self.user
        )

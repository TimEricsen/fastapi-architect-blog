from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base


class Favourite(Base):
    __tablename__ = 'favourites'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    __table_args__ = (UniqueConstraint('post_id', 'username', name='post_user_uc_favourites'),)

    user = relationship('User', back_populates='favourites')
    post = relationship('Post', back_populates='favourites')

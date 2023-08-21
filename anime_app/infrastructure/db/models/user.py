from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base
from anime_app.core.models import dto


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, unique=True)
    creation_date = Column(Date, nullable=True)

    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='username')
    comment_likes = relationship('CommentLike', back_populates='username')
    favourites = relationship('Favourite', back_populates='user', cascade='all,delete')

    def to_dto(self) -> dto.MainUser:
        return dto.MainUser(
            id=self.id,
            username=self.username,
            email=self.email,
            creation_date=self.creation_date,
            hashed_password=self.hashed_password
        )

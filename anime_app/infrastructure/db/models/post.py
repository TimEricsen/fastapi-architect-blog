from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base
from anime_app.core.models import dto


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(Text)
    author = Column(String, ForeignKey('users.username', ondelete='cascade'))
    publication_date = Column(DateTime, nullable=True)

    complaints = relationship('Complaint', back_populates='post', cascade='all,delete')
    likes = relationship('Like', back_populates='post', cascade='all,delete')
    favourites = relationship('Favourite', back_populates='post', cascade='all,delete')
    comments = relationship('Comment', back_populates='post', lazy='selectin', cascade='all,delete')

    def to_dto(self) -> dto.MainPost:
        return dto.MainPost(
            id=self.id,
            title=self.title,
            description=self.description,
            author=self.author,
            publication_date=self.publication_date,
            likes=len(self.likes)
        )

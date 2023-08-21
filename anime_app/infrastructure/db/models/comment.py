from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, backref

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.base import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(String, ForeignKey('users.username', ondelete='SET DEFAULT'), server_default='Deleted Account!')
    post_id = Column(Integer, ForeignKey('posts.id'))
    time_posted = Column(DateTime)
    answer_to = Column(Integer, ForeignKey('comments.id', ondelete='cascade'), nullable=True)

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')
    likes = relationship('CommentLike', back_populates='comment', cascade='all,delete')
    complaints = relationship('ComplaintComment', back_populates='comment', cascade='all,delete')
    answers = relationship('Comment', backref=backref('parent', remote_side=[id]),
                           lazy='selectin', cascade="all,delete")

    def to_dto(self) -> dto.ParentComment:
        return dto.ParentComment(
            text=self.text,
            answer_to=self.answer_to,
            author=self.author,
            time_posted=self.time_posted,
            post_id=self.post_id
        )

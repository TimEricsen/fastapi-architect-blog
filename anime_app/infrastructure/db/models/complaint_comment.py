from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.base import Base


class ComplaintComment(Base):
    __tablename__ = 'complaint_comment'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    reason = Column(String, nullable=False)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    user = Column(String, ForeignKey('users.username'))

    comment = relationship('Comment', back_populates='complaints')

    __table_args__ = (UniqueConstraint('comment_id', 'user', name='comment_user_complaint_uc'),)

    def to_dto(self) -> dto.MainCommentComplaint:
        return dto.MainCommentComplaint(
            id=self.id,
            comment_id=self.comment_id,
            user=self.user,
            reason=self.reason
        )

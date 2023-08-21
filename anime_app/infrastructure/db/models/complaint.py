from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from anime_app.infrastructure.db.models.base import Base
from anime_app.core.models import dto


class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    reason = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='cascade'))
    user = Column(String, ForeignKey('users.username', ondelete='cascade'))

    post = relationship('Post', back_populates='complaints')

    __table_args__ = (UniqueConstraint('post_id', 'user', name='post_user_complaint_uc'),)

    def to_dto(self) -> dto.MainComplaint:
        return dto.MainComplaint(
            id=self.id,
            reason=self.reason,
            post_id=self.post_id,
            user=self.user
        )

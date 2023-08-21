from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

from anime_app.infrastructure.db.models.base import Base


class BL(Base):
    __tablename__ = 'black_list'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, ForeignKey('users.username'))
    user_id = Column(Integer, ForeignKey('users.id'))

    __table_args__ = (UniqueConstraint('username', 'user_id', name='username_user_id_uc'),)

from sqlalchemy.ext.asyncio import AsyncSession

from anime_app.infrastructure.dao.user import UserDAO
from anime_app.infrastructure.dao.post import PostDao
from anime_app.infrastructure.dao.like import LikeDao
from anime_app.infrastructure.dao.comment import CommentDao
from anime_app.infrastructure.dao.comment_like import CommentLikeDAO
from anime_app.infrastructure.dao.favourites import FavouriteDAO
from anime_app.infrastructure.dao.black_list import BLDAO
from anime_app.infrastructure.dao.complaint import ComplaintDAO
from anime_app.infrastructure.dao.complaint_comment import ComplaintCommentDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = UserDAO(self.session)
        self.post = PostDao(self.session)
        self.like = LikeDao(self.session)
        self.comment = CommentDao(self.session)
        self.favourite = FavouriteDAO(self.session)
        self.bl = BLDAO(self.session)
        self.complaint = ComplaintDAO(session)
        self.comment_like = CommentLikeDAO(session)
        self.complaint_comment = ComplaintCommentDAO(session)

    async def commit(self):
        await self.session.commit()

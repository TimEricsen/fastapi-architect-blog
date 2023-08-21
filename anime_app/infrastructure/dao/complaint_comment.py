from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql.asyncpg import exc
from sqlalchemy.exc import NoResultFound

from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.complaint_comment import ComplaintComment
from anime_app.core.models import dto
from anime_app.infrastructure.db.models.comment import Comment
from anime_app.core.utils.exceptions.complaint import SelfComplaintException, AlreadyComplainedException
from anime_app.core.utils.exceptions.post import PostOrCommentNotFoundException


class ComplaintCommentDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(ComplaintComment, session)

    async def add_comment_complaint(self, post_id: int, comment_id: int, username: int,
                                    reason: dto.CreateCommentComplaint) -> str:
        comment = await self.session.execute(select(Comment).where(
            Comment.post_id == post_id, Comment.id == comment_id))
        try:
            comment = comment.scalar_one()
            if comment.author == username:
                raise SelfComplaintException

            new_complaint = ComplaintComment(
                comment_id=comment_id,
                user=username,
                reason=reason.reason.value,
            )
            self.session.add(new_complaint)
            await self.commit()
            await self.session.refresh(new_complaint)
            return 'Thanks for the help! We will definitely look into your complaint!'

        except exc.IntegrityError:
            raise AlreadyComplainedException

        except NoResultFound:
            raise PostOrCommentNotFoundException

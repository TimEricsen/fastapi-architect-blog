from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql.asyncpg import exc

from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.comment_like import CommentLike
from anime_app.infrastructure.db.models.comment import Comment
from anime_app.core.utils.exceptions.post import PostOrCommentNotFoundException


class CommentLikeDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(CommentLike, session)

    async def remove_like_comment(self, comment_id: int, username: str):
        await self.session.rollback()
        query = await self.session.execute(select(CommentLike).where(
            CommentLike.comment_id == comment_id, CommentLike.user == username))
        result = query.scalar_one()
        await self.session.delete(result)
        await self.session.commit()
        return 'Your like has been removed!'

    async def like_comment(self, post_id: int, comment_id: int, username: str):
        comment = await self.session.execute(select(Comment).where(
            Comment.post_id == post_id, Comment.id == comment_id))
        try:
            comment.scalar_one()
            new_like = CommentLike(
                comment_id=comment_id,
                user=username
            )
            self.session.add(new_like)
            await self.commit()
            await self.session.refresh(new_like)
            return 'Your like has been added!'

        except exc.IntegrityError:
            return await self.remove_like_comment(comment_id, username)

        except NoResultFound:
            raise PostOrCommentNotFoundException

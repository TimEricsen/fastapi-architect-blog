from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql.asyncpg import exc

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.like import Like
from anime_app.infrastructure.db.models.post import Post
from anime_app.infrastructure.db.models.comment import Comment
from anime_app.infrastructure.db.models.comment_like import CommentLike
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.core.utils.exceptions.like import LikesNotFoundException


class LikeDao(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Like, session)

    async def remove_like_post(self, post_id: int, username: str) -> str:
        await self.rollback()
        query = await self.session.execute(select(Like).where(
            Like.post_id == post_id, Like.user == username))
        result = query.scalar_one()
        await self.session.delete(result)
        await self.session.commit()
        return 'Your like has been removed!'

    async def like_post(self, post_id: int, username: str) -> str:
        try:
            new_like = Like(
                post_id=post_id,
                user=username
            )
            self.session.add(new_like)
            await self.commit()
            await self.session.refresh(new_like)
            return 'Your like has been added!'
        except exc.IntegrityError:
            return await self.remove_like_post(post_id, username)

    async def my_likes(self, username: str):
        result = {}

        post_query = await self.session.execute(select(Post).options(
            selectinload(Post.likes)).where(Post.likes.any(Like.user == username)))
        posts = [post.to_dto() for post in post_query.scalars().all()]
        if posts:
            result['posts'] = posts

        comment_query = await self.session.execute(select(Comment).options(
            selectinload(Comment.likes)).where(Comment.likes.any(CommentLike.user == username)))
        comments = [dto.MainComment(
                text=comment.text,
                author=comment.author,
                time_posted=comment.time_posted,
                post_id=comment.post_id,
                likes=len(comment.likes)
            ) for comment in comment_query.scalars().all()]
        if comments:
            result['comments'] = comments

        if not result:
            raise LikesNotFoundException
        return result

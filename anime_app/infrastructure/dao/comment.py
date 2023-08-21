import re

from typing import List
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.comment import Comment
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.core.utils.exceptions.comment import CommentNotFoundOrNotCreatorException, CommentsNotFoundException
from anime_app.core.utils.exceptions.post import PostOrCommentNotFoundException, NotPostOwnerException
from anime_app.core.utils.exceptions.base import InaccessibleCharactersException


class CommentDao(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def add_comment(self, post_id: int, comment: dto.CreateComment,
                          answer_to: int, username: str) -> dto.MainComment:
        check_comment = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", comment.text)
        if check_comment:
            if not answer_to:
                new_comment = Comment(
                    text=comment.text,
                    author=username,
                    post_id=post_id,
                    time_posted=datetime.utcnow()
                )
                self.session.add(new_comment)
                await self.commit()
                await self.session.refresh(new_comment)
                return new_comment.to_dto()
            else:
                parent_comment = await self.session.execute(select(Comment).where(
                    Comment.id == answer_to, Comment.post_id == post_id))
                try:
                    parent_result = parent_comment.scalar_one()  # noqa F841
                except NoResultFound:
                    raise PostOrCommentNotFoundException
                new_comment = Comment(
                        text=comment.text,
                        author=username,
                        post_id=post_id,
                        time_posted=datetime.utcnow(),
                        answer_to=answer_to
                    )
                self.session.add(new_comment)
                await self.commit()
                await self.session.refresh(new_comment)
                return new_comment.to_dto()
        else:
            raise InaccessibleCharactersException

    async def get_pk_comments(self, pk: int) -> dto.ParentComment:
        query = await self.session.execute(
            select(Comment).options(selectinload(Comment.answers), selectinload(Comment.likes)).where(
                Comment.id == pk).order_by(Comment.time_posted))
        result = query.scalar_one()
        answers = [await self.get_pk_comments(answer.id) for answer in result.answers]

        return dto.ParentComment(
            text=result.text,
            author=result.author,
            time_posted=result.time_posted,
            post_id=result.post_id,
            likes=len(result.likes),
            answers=answers if result.answers else None
        )

    async def update_comment(self, post_id: int, comment_id: int, editable_comment: dto.EditComment,
                             username: str) -> str:
        comment = await self.session.execute(select(Comment).where(
            Comment.id == comment_id, Comment.author == username, Comment.post_id == post_id))
        try:
            comment = comment.scalar_one()  # noqa F841
        except NoResultFound:
            raise CommentNotFoundOrNotCreatorException

        check_comment = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", editable_comment.text)
        if check_comment:
            updating = update(Comment).where(Comment.id == comment_id, Comment.author == username).values(
                text=editable_comment.text).execution_options(synchronize_session='fetch')
            query = await self.session.execute(updating)  # noqa F841
            await self.commit()
            return 'Your comment was updated!'
        else:
            raise InaccessibleCharactersException

    async def delete_comment(self, post_id: int, comment_id: int, username: str, post_author: str) -> str:
        comment = await self.session.execute(select(Comment).where(
            Comment.id == comment_id, Comment.post_id == post_id))
        try:
            result = comment.scalar_one()
            if result.author == username or post_author == username:
                await self.session.delete(result)
                await self.commit()
                return 'Comment was deleted!'
            else:
                raise NotPostOwnerException
        except NoResultFound:
            raise CommentNotFoundOrNotCreatorException

    async def my_comments(self, username: str) -> List[dto.MainComment]:
        query = await self.session.execute(select(Comment).options(
            selectinload(Comment.likes)).where(Comment.author == username))
        comments = query.scalars().all()
        if comments:
            return [dto.MainComment(
                text=comment.text,
                author=comment.author,
                time_posted=comment.time_posted,
                post_id=comment.post_id,
                likes=len(comment.likes)
            ) for comment in comments]
        raise CommentsNotFoundException

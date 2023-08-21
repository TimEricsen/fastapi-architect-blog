import re

from typing import List
from sqlalchemy import select, func, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from anime_app.core.models import dto
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.post import Post
from anime_app.core.utils.exceptions.post import PostIDNotFoundException, NotPositivePostIDException, \
    EmptyPostListException, NotPostOwnerException, PostNotFoundOrNotCreatorException
from anime_app.core.utils.exceptions.base import InaccessibleCharactersException


class PostDao(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    async def get_all_posts(self) -> List[dto.MainPost]:
        query = await self.session.execute(select(Post).options(selectinload(Post.likes)).order_by(
            Post.publication_date.desc()))
        try:
            result = query.scalars().all()
            return [post.to_dto() for post in result]
        except NoResultFound:
            raise EmptyPostListException

    async def get_post_by_id(self, post_id: int) -> dto.MainPost:
        if isinstance(post_id, int) and post_id > 0:
            query = await self.session.execute(select(Post).options(selectinload(Post.likes)).where(Post.id == post_id))
            try:
                result = query.scalar_one()
                return result.to_dto()
            except NoResultFound:
                raise PostIDNotFoundException(post_id)
        else:
            raise NotPositivePostIDException

    async def get_post_by_query_search(self, search: str) -> List[dto.MainPost]:
        query = await self.session.execute(select(Post).options(selectinload(Post.likes)).where(
            func.lower(Post.title).like(f'%{search.lower()}%')))
        result = query.scalars().all()
        if not result:
            raise EmptyPostListException
        return [post.to_dto() for post in result]

    async def get_my_posts(self, username: str) -> List[dto.MainPost]:
        query = await self.session.execute(select(Post).options(
            selectinload(Post.likes)).where(Post.author == username))
        result = query.scalars().all()
        if not result:
            raise EmptyPostListException
        return [post.to_dto() for post in result]

    async def update_post(self, post: dto.UpdatePost, post_id: int, username: str) -> str:
        checking = await self.get_post_by_id(post_id)
        if not checking.author == username:
            raise NotPostOwnerException
        query = update(Post).where(Post.id == post_id, Post.author == username)
        if post.title:
            check_title = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", post.title)
            if check_title:
                query = query.values(title=post.title)
            else:
                raise InaccessibleCharactersException
        if post.description:
            check_description = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", post.description)
            if check_description:
                query = query.values(description=post.description)
            else:
                raise InaccessibleCharactersException
        query = query.execution_options(synchronize_session='fetch')
        await self.session.execute(query)
        await self.session.commit()
        return 'Post updated!'

    async def delete_post(self, post_id: int, username: str) -> str:
        query = await self.session.execute(select(Post).where(
            Post.id == post_id, Post.author == username))
        try:
            result = query.scalar_one()
            await self.session.delete(result)
            await self.commit()
            return 'This post was successfully deleted!'
        except NoResultFound:
            raise PostNotFoundOrNotCreatorException

    async def get_post_with_comments_by_id(self, post_id: int):
        if isinstance(post_id, int) and post_id > 0:
            query = await self.session.execute(select(Post).options(
                selectinload(Post.comments), selectinload(Post.likes)).where(Post.id == post_id))
            try:
                result = query.scalar_one()
                return result
            except NoResultFound:
                raise PostIDNotFoundException(post_id)
        else:
            raise NotPositivePostIDException

    async def add_new_post(self, new_post) -> None:
        self.session.add(new_post)

    async def refresh_new_post(self, new_post) -> None:
        await self.session.refresh(new_post)

    async def return_post_by_id(self, post, comments) -> dto.MainRetrievePost:
        return dto.MainRetrievePost(
            id=post.id,
            title=post.title,
            description=post.description,
            author=post.author,
            publication_date=post.publication_date,
            likes=[like.to_dto() for like in post.likes],
            comments=comments
        )

    async def user_posts(self, author: str) -> List[dto.MainPost]:
        query = await self.session.execute(select(Post).options(selectinload(Post.likes)).where(Post.author == author))
        result = query.scalars().all()
        if not result:
            raise EmptyPostListException
        return [post.to_dto() for post in result]

    async def check_post_existence(self, post_id: int) -> None:
        query = await self.session.execute(select(Post).where(Post.id == post_id))
        result = query.scalar_one_or_none()
        if result is None:
            raise PostIDNotFoundException(post_id)

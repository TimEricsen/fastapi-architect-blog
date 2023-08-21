from sqlalchemy import select
from typing import List, Union
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql.asyncpg import exc

from anime_app.core.models import dto
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.post import Post
from anime_app.infrastructure.db.models.user import User
from anime_app.infrastructure.db.models.favourites import Favourite
from anime_app.core.utils.exceptions.favourites import PostAlreadyInFavouritesException, PostNotInFavouritesException


class FavouriteDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Favourite, session)

    async def add_to_favourites(self, post_id: int, username: str) -> str:
        try:
            new_favourite = Favourite(
                username=username,
                post_id=post_id
            )
            self.session.add(new_favourite)
            await self.commit()
            await self.session.refresh(new_favourite)
            return 'Added to favourites!'
        except exc.IntegrityError:
            raise PostAlreadyInFavouritesException(post_id)

    async def delete_from_favourites(self, post_id: int, username: str) -> str:
        favourite = await self.session.execute(select(Favourite).where(
            Favourite.post_id == post_id, Favourite.username == username))
        try:
            result = favourite.scalar_one()
            await self.session.delete(result)
            await self.commit()
            return 'Post deleted from favourites!'
        except NoResultFound:
            raise PostNotInFavouritesException(post_id)

    async def my_favourites(self, username: str) -> Union[List[dto.MainPost], str]:
        query = await self.session.execute(select(Post).options(
            selectinload(Post.favourites), selectinload(Post.likes)).where(Post.favourites.any(username=username)))
        result = query.scalars().all()
        if result:
            return [post.to_dto() for post in result]
        return 'Your favourites list is empty!'

    async def remove_posts_from_favourites_if_added_to_black_list(self, user_id: int, post_author: str) -> None:
        query = await self.session.execute(select(Favourite).options(
            selectinload(Favourite.post), selectinload(Favourite.user)).where(
            Favourite.post.has(Post.author == post_author), Favourite.user.has(User.id == user_id)))
        result = query.scalars().all()
        for fav in result:
            await self.session.delete(fav)
            await self.commit()

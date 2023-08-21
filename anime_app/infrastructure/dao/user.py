from typing import List
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.user import User
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.core.utils.exceptions.user import UserIDNotFoundException


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> dto.MainUser:
        result = await self.session.execute(
            select(User).where(User.username == username))
        try:
            user = result.scalar_one()
            return user.to_dto()
        except NoResultFound:
            pass

    async def get_by_email(self, email: str) -> dto.MainUser:
        result = await self.session.execute(
            select(User).where(User.email == email))
        try:
            user = result.scalar_one()
            return user.to_dto()
        except NoResultFound:
            pass

    async def get_by_id(self, user_id: int) -> dto.BLUser:
        result = await self.session.execute(
            select(User).where(User.id == user_id))
        try:
            user = result.scalar_one()
            return dto.BLUser(
                id=user.id,
                username=user.username,
                email=user.email
            )
        except NoResultFound:
            raise UserIDNotFoundException(user_id)

    async def check_user_by_id(self, user_id: int) -> None:
        if not await self.check_by_id(user_id):
            raise UserIDNotFoundException(user_id)
        pass

    async def get_users_from_bl(self, black_list) -> List[dto.BLUser]:
        return [await self.get_by_id(user.user_id) for user in black_list]

    async def add_new_user(self, new_user) -> None:
        self.session.add(new_user)

    async def refresh_new_user(self, new_user) -> None:
        await self.session.refresh(new_user)

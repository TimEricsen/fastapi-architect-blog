from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql.asyncpg import exc

from anime_app.core.models import dto
from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.black_list import BL
from anime_app.core.utils.exceptions.black_list import SelfAddToBLException, UserAlreadyInBLException, \
    UserNotInBLException, EmptyBLException


class BLDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(BL, session)

    async def add_to_bl(self, user_id: int, current_user: dto.MainUser) -> str:
        if current_user.id == user_id:
            raise SelfAddToBLException
        try:
            new_bl_user = BL(
                username=current_user.username,
                user_id=user_id
            )
            self.session.add(new_bl_user)
            await self.commit()
            await self.session.refresh(new_bl_user)
            return f'You added user with id {user_id} to black list'
        except exc.IntegrityError:
            raise UserAlreadyInBLException(user_id)

    async def remove_from_bl(self, user_id: int, current_user: dto.MainUser) -> str:
        if current_user.id == user_id:
            raise SelfAddToBLException
        query = await self.session.execute(select(BL).where(
            BL.user_id == user_id, BL.username == current_user.username))
        try:
            result = query.scalar_one()
            await self.session.delete(result)
            await self.commit()
            return 'You removed this user from black list!'
        except NoResultFound:
            raise UserNotInBLException(user_id)

    async def if_in_black_list(self, user_id: int, username: str) -> bool:
        query = await self.session.execute(select(BL).where(BL.username == username, BL.user_id == user_id))
        return query.scalar_one_or_none() is None

    async def my_bl(self, current_user: dto.MainUser):
        query = await self.session.execute(select(BL).where(BL.username == current_user.username))
        result = query.scalars().all()
        if not result:
            raise EmptyBLException
        return result

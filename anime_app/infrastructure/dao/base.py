from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int):
        query = await self.session.execute(select(self.model).where(self.model.id == id_))
        result = query.scalar_one_or_none()
        return result

    async def check_by_id(self, id_: int) -> bool:
        query = await self.session.execute(select(self.model).where(self.model.id == id_))
        result = query.scalar_one_or_none()
        return result is not None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

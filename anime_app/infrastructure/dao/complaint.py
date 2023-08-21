from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql.asyncpg import exc

from anime_app.infrastructure.dao.base import BaseDAO
from anime_app.infrastructure.db.models.complaint import Complaint
from anime_app.core.models import dto
from anime_app.core.utils.exceptions.complaint import AlreadyComplainedException


class ComplaintDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Complaint, session)

    async def create_complaint(self, post_id: int, username: str, complaint: dto.CreateComplaint):
        try:
            new_complaint = Complaint(
                reason=complaint.reason.value,
                post_id=post_id,
                user=username
            )
            self.session.add(new_complaint)
            await self.commit()
            await self.session.refresh(new_complaint)
            return 'Thanks for the help! We will definitely look into your complaint!'

        except exc.IntegrityError:
            raise AlreadyComplainedException

from anime_app.core.models import dto
from anime_app.core.interfaces.dal.complaint import ComplaintCreator


async def add_complaint(post_id: int, username: str,
                        complaint: dto.CreateComplaint, dao: ComplaintCreator) -> str:
    return await dao.create_complaint(post_id, username, complaint)

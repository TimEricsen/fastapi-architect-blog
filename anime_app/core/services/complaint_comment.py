from anime_app.core.models import dto
from anime_app.core.interfaces.dal.complaint_comment import CommentComplaintAdder


async def add_comment_complaint(post_id: int, comment_id: int, username: str,
                                reason: dto.CreateCommentComplaint, dao: CommentComplaintAdder) -> str:
    return await dao.add_comment_complaint(post_id, comment_id, username, reason)

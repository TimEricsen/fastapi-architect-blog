from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.services.complaint_comment import add_comment_complaint


router = APIRouter(tags=['Complaint'])


@router.post('/posts/post/{post_id}/comment/{comment_id}/complaint')
async def make_comment_complaint(post_id: int, comment_id: int, reason: dto.CreateCommentComplaint,
                                 current_user: dto.MainUser = Depends(get_current_user),
                                 dao: HolderDao = Depends(dao_provider)) -> str:
    return await add_comment_complaint(post_id, comment_id, current_user.username, reason, dao.complaint_comment)

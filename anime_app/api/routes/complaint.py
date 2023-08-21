from fastapi import APIRouter, Depends

from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.api.dependencies.db import dao_provider
from anime_app.core.services.complaint import add_complaint
from anime_app.core.models import dto
from anime_app.core.services.post import get_simple_post_by_id
from anime_app.core.services.black_list import check_black_list
from anime_app.core.utils.exceptions.black_list import UserInBLException
from anime_app.core.utils.exceptions.complaint import SelfComplaintException


router = APIRouter()


@router.post('/posts/post/{post_id}/complaint', tags=['Complaint'])
async def make_complaint(post_id: int,
                         complaint: dto.CreateComplaint,
                         dao: HolderDao = Depends(dao_provider),
                         current_user: dto.MainUser = Depends(get_current_user)) -> str:
    post = await get_simple_post_by_id(post_id, dao.post)
    if post.author == current_user.username:
        raise SelfComplaintException
    if not await check_black_list(current_user.id, post.author, dao.bl):
        raise UserInBLException
    return await add_complaint(post_id, current_user.username, complaint, dao.complaint)

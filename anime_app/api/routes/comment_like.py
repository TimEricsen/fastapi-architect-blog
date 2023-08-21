from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.services.comment_like import comment_like


router = APIRouter(tags=['Like'])


@router.get('/posts/post/{post_id}/comment/{comment_id}/like')
async def like_comment(post_id: int, comment_id: int,
                       current_user: dto.MainUser = Depends(get_current_user),
                       dao: HolderDao = Depends(dao_provider)) -> str:
    return await comment_like(post_id, comment_id, current_user.username, dao.comment_like)

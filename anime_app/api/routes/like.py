from fastapi import APIRouter, Depends

from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.db import dao_provider
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.models import dto
from anime_app.core.services.post import get_simple_post_by_id
from anime_app.core.services.black_list import check_black_list
from anime_app.core.services.like import post_like, get_my_likes
from anime_app.core.utils.exceptions.black_list import UserInBLException


router = APIRouter(tags=['Like'])


@router.get('/posts/post/{post_id}/like')
async def like_post(post_id: int,
                    current_user: dto.MainUser = Depends(get_current_user),
                    dao: HolderDao = Depends(dao_provider)) -> str:
    post = await get_simple_post_by_id(post_id, dao.post)
    if not await check_black_list(current_user.id, post.author, dao.bl):
        raise UserInBLException
    return await post_like(post_id, current_user.username, dao.like)


@router.get('/user/me/likes')
async def my_likes(current_user: dto.MainUser = Depends(get_current_user),
                   dao: HolderDao = Depends(dao_provider)):
    return await get_my_likes(current_user.username, dao.like)

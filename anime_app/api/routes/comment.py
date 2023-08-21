from typing import Union, List
from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.services.post import get_simple_post_by_id, check_post_existence
from anime_app.core.services.black_list import check_black_list
from anime_app.core.services.comment import comment_add, comment_edit, comment_delete, get_my_comments
from anime_app.core.utils.exceptions.black_list import UserInBLException


router = APIRouter(tags=['Comment'])


@router.post('/posts/post/{post_id}/comment/add')
async def add_comment(post_id: int, comment: dto.CreateComment, answer_to: Union[int, None] = None,
                      current_user: dto.MainUser = Depends(get_current_user),
                      dao: HolderDao = Depends(dao_provider)) -> dto.MainComment:
    post = await get_simple_post_by_id(post_id, dao.post)
    if not await check_black_list(current_user.id, post.author, dao.bl):
        raise UserInBLException
    return await comment_add(post_id, comment, current_user.username, answer_to, dao.comment)


@router.patch('/posts/post/{post_id}/comment/{comment_id}/edit')
async def edit_comment(post_id: int, comment_id: int, editable_comment: dto.EditComment,
                       current_user: dto.MainUser = Depends(get_current_user),
                       dao: HolderDao = Depends(dao_provider)) -> str:
    await check_post_existence(post_id, dao.post)
    return await comment_edit(post_id, comment_id, editable_comment, current_user.username, dao.comment)


@router.delete('/posts/post/{post_id}/comment/{comment_id}/delete')
async def delete_comment(post_id: int, comment_id: int,
                         current_user: dto.MainUser = Depends(get_current_user),
                         dao: HolderDao = Depends(dao_provider)) -> str:
    post = await get_simple_post_by_id(post_id, dao.post)
    return await comment_delete(post_id, comment_id, current_user.username, post.author, dao.comment)


@router.get('/user/me/comments')
async def my_comments(current_user: dto.MainUser = Depends(get_current_user),
                      dao: HolderDao = Depends(dao_provider)) -> List[dto.MainComment]:
    return await get_my_comments(current_user.username, dao.comment)

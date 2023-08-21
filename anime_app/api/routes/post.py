from typing import List
from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user, get_current_user_or_pass
from anime_app.api.dependencies.db import dao_provider
from anime_app.core.services.post import post_create, get_posts_all, get_by_id_post, return_post_by_id, \
    get_posts_query_search, get_my_post_list, post_update, post_delete, posts_by_user
from anime_app.core.services.black_list import check_black_list
from anime_app.core.services.comment import get_comments_for_post
from anime_app.core.services.user import get_user_by_id
from anime_app.core.utils.exceptions.black_list import UserInBLException


router = APIRouter(tags=['Post'])


@router.post('/posts/create', response_model_exclude_none=dto.MainPost)
async def create_post(post: dto.CreatePost,
                      dao: HolderDao = Depends(dao_provider),
                      current_user: dto.MainUser = Depends(get_current_user)) -> dto.MainPost:
    return await post_create(post, dao.post, current_user)


@router.get('/posts/all')
async def get_all_posts(dao: HolderDao = Depends(dao_provider)) -> List[dto.MainPost]:
    return await get_posts_all(dao.post)


@router.get('/posts/post/{post_id}')
async def get_post_by_id(post_id: int, current_user: dto.MainUser = Depends(get_current_user_or_pass),
                         dao: HolderDao = Depends(dao_provider)):
    post = await get_by_id_post(post_id, dao.post)
    if current_user:
        if not await check_black_list(current_user.id, post.author, dao.bl):
            raise UserInBLException
    comments = await get_comments_for_post(post, dao.comment)
    return await return_post_by_id(post, comments, dao.post)


@router.get('/posts')
async def get_posts_by_query_search(search: str, dao: HolderDao = Depends(dao_provider)) -> List[dto.MainPost]:
    return await get_posts_query_search(search, dao.post)


@router.get('/posts/my')
async def get_my_posts(dao: HolderDao = Depends(dao_provider),
                       current_user: dto.MainUser = Depends(get_current_user)) -> List[dto.MainPost]:
    return await get_my_post_list(current_user.username, dao.post)


@router.patch('/posts/post/{post_id}/update')
async def update_post(post: dto.UpdatePost,
                      post_id: int, dao: HolderDao = Depends(dao_provider),
                      current_user: dto.MainUser = Depends(get_current_user)) -> str:
    return await post_update(post, post_id, dao.post, current_user.username)


@router.delete('/posts/post/{post_id}/delete')
async def delete_post(post_id: int,
                      dao: HolderDao = Depends(dao_provider),
                      current_user: dto.MainUser = Depends(get_current_user)) -> str:
    return await post_delete(post_id, current_user.username, dao.post)


@router.get('/user/{user_id}/posts')
async def user_posts(user_id: int, dao: HolderDao = Depends(dao_provider)) -> List[dto.MainPost]:
    user = await get_user_by_id(user_id, dao.user)
    return await posts_by_user(user.username, dao.post)

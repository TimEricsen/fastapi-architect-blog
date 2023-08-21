from typing import List, Union
from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.services.post import get_simple_post_by_id, check_post_existence
from anime_app.core.services.black_list import check_black_list
from anime_app.core.services.favourites import favourites_add, favourites_delete, get_my_favourites
from anime_app.core.utils.exceptions.black_list import UserInBLException


router = APIRouter(tags=['Favourites'])


@router.get('/posts/post/{post_id}/add-to-favourites')
async def add_to_favourites(post_id: int,
                            current_user: dto.MainUser = Depends(get_current_user),
                            dao: HolderDao = Depends(dao_provider)) -> str:
    post = await get_simple_post_by_id(post_id, dao.post)
    if not await check_black_list(current_user.id, post.author, dao.bl):
        raise UserInBLException
    return await favourites_add(post_id, current_user.username, dao.favourite)


@router.delete('/posts/post/{post_id}/delete-from-favourites')
async def delete_from_favourites(post_id: int,
                                 current_user: dto.MainUser = Depends(get_current_user),
                                 dao: HolderDao = Depends(dao_provider)) -> str:
    await check_post_existence(post_id, dao.post)
    return await favourites_delete(post_id, current_user.username, dao.favourite)


@router.get('/user/me/favourites')
async def my_favourites(current_user: dto.MainUser = Depends(get_current_user),
                        dao: HolderDao = Depends(dao_provider)) -> Union[List[dto.MainPost], str]:
    return await get_my_favourites(current_user.username, dao.favourite)

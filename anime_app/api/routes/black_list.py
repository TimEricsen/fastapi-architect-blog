from typing import List
from fastapi import APIRouter, Depends

from anime_app.core.models import dto
from anime_app.api.dependencies.db import dao_provider
from anime_app.infrastructure.dao.holder import HolderDao
from anime_app.api.dependencies.auth import get_current_user
from anime_app.core.services.black_list import add_to_bl, remove_from_bl, my_black_list
from anime_app.core.services.user import check_user_existence, get_users_from_black_list
from anime_app.core.services.favourites import remove_posts_from_favourites_if_added_to_bl


router = APIRouter(tags=['Black List'])


@router.get('/add-to-black-list/{user_id}')
async def add_to_black_list(user_id: int,
                            current_user: dto.MainUser = Depends(get_current_user),
                            dao: HolderDao = Depends(dao_provider)):
    await check_user_existence(user_id, dao.user)
    result = await add_to_bl(user_id, current_user, dao.bl)
    await remove_posts_from_favourites_if_added_to_bl(user_id, current_user.username, dao.favourite)
    return result


@router.delete('/delete-from-black-list/{user_id}')
async def remove_from_black_list(user_id: int,
                                 current_user: dto.MainUser = Depends(get_current_user),
                                 dao: HolderDao = Depends(dao_provider)) -> str:
    await check_user_existence(user_id, dao.user)
    return await remove_from_bl(user_id, current_user, dao.bl)


@router.get('/user/me/black-list')
async def get_my_black_list(current_user: dto.MainUser = Depends(get_current_user),
                            dao: HolderDao = Depends(dao_provider)) -> List[dto.BLUser]:
    black_list = await my_black_list(current_user, dao.bl)
    return await get_users_from_black_list(black_list, dao.user)

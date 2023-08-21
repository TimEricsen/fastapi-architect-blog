from typing import List, Union

from anime_app.core.interfaces.dal.favourites import FromFavouriteBlackListDeleter, FavouriteAdder, FavouriteDeleter, \
    MyFavouritesGetter
from anime_app.core.models import dto


async def remove_posts_from_favourites_if_added_to_bl(user_id: int, post_author: str,
                                                      dao: FromFavouriteBlackListDeleter) -> None:
    return await dao.remove_posts_from_favourites_if_added_to_black_list(user_id, post_author)


async def favourites_add(post_id: int, username: str, dao: FavouriteAdder) -> str:
    return await dao.add_to_favourites(post_id, username)


async def favourites_delete(post_id: int, username: str, dao: FavouriteDeleter) -> str:
    return await dao.delete_from_favourites(post_id, username)


async def get_my_favourites(username: str, dao: MyFavouritesGetter) -> Union[List[dto.MainPost], str]:
    return await dao.my_favourites(username)

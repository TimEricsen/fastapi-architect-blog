from anime_app.core.models import dto
from anime_app.core.interfaces.dal.black_list import BlackListAdder, BlackListDeleter, MyBlackListGetter, \
    UserInBlackListChecker


async def add_to_bl(user_id: int, current_user: dto.MainUser,
                    dao: BlackListAdder) -> str:
    return await dao.add_to_bl(user_id, current_user)


async def remove_from_bl(user_id: int, current_user: dto.MainUser,
                         dao: BlackListDeleter) -> str:
    return await dao.remove_from_bl(user_id, current_user)


async def my_black_list(current_user: dto.MainUser, dao: MyBlackListGetter):
    return await dao.my_bl(current_user)


async def check_black_list(user_id: int, username: str, dao: UserInBlackListChecker) -> bool:
    return await dao.if_in_black_list(user_id, username)

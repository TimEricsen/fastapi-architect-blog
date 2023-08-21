from typing import Protocol, List


from anime_app.core.models import dto
from anime_app.core.interfaces.dal.base import Committer


class BlackListAdder(Committer, Protocol):
    async def add_to_bl(self, user_id: int, current_user: dto.MainUser) -> str:
        raise NotImplementedError


class BlackListDeleter(Committer, Protocol):
    async def remove_from_bl(self, user_id: int, current_user: dto.MainUser) -> str:
        raise NotImplementedError


class MyBlackListGetter(Committer, Protocol):
    async def my_bl(self, current_user: dto.MainUser) -> List[dto.BLUser]:
        raise NotImplementedError


class UserInBlackListChecker(Protocol):
    async def if_in_black_list(self, user_id: int, username: str) -> bool:
        raise NotImplementedError

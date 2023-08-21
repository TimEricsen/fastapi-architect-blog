from anime_app.infrastructure.dao.holder import HolderDao


def dao_provider() -> HolderDao:
    raise NotImplementedError


class DBProvider:
    def __init__(self, pool):
        self.pool = pool

    async def dao(self):
        async with self.pool() as session:
            yield HolderDao(session=session)

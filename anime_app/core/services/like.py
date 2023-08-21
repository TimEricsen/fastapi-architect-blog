from anime_app.core.interfaces.dal.like import LikeCreator, MyLikesGetter


async def post_like(post_id: int, username: str, dao: LikeCreator) -> str:
    return await dao.like_post(post_id, username)


async def get_my_likes(username: str, dao: MyLikesGetter):
    return await dao.my_likes(username)

from anime_app.core.interfaces.dal.comment_like import CommentLikeCreator


async def comment_like(post_id: int, comment_id: int, username: str, dao: CommentLikeCreator):
    return await dao.like_comment(post_id, comment_id, username)

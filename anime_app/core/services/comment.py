from typing import Union, List

from anime_app.core.interfaces.dal.comment import CommentsForPostGetter, CommentAdder, CommentEditor, CommentDeleter, \
    MyCommentGetter
from anime_app.core.models import dto


async def get_comments_for_post(post_model, dao: CommentsForPostGetter):
    return [await dao.get_pk_comments(comment.id)
            for comment in post_model.comments if comment.answer_to is None]


async def comment_add(post_id: int, comment: dto.CreateComment, username: str,
                      answer_to: Union[int, None], dao: CommentAdder) -> dto.MainComment:
    return await dao.add_comment(post_id, comment, answer_to, username)


async def comment_edit(post_id: int, comment_id: int, editable_comment: dto.EditComment,
                       username: str, dao: CommentEditor) -> str:
    return await dao.update_comment(post_id, comment_id, editable_comment, username)


async def comment_delete(post_id: int, comment_id: int, username: str, post_author, dao: CommentDeleter) -> str:
    return await dao.delete_comment(post_id, comment_id, username, post_author)


async def get_my_comments(username: str, dao: MyCommentGetter) -> List[dto.MainComment]:
    return await dao.my_comments(username)

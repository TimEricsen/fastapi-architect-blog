import re

from typing import List
from datetime import datetime

from anime_app.core.models import dto
from anime_app.infrastructure.db.models.post import Post
from anime_app.core.interfaces.dal.post import PostCreator, AllPostsGetter, PostByIDGetter, PostByIDReturner, \
    PostsByQuerySearchGetter, MyPostsGetter, PostUpdater, PostDeleter, PostByUserGetter, SimplePostGetter, \
    PostExistenceChecker
from anime_app.core.utils.exceptions.base import InaccessibleCharactersException


async def post_create(post: dto.CreatePost,
                      dao: PostCreator,
                      current_user: dto.MainUser) -> dto.MainPost:
    check_title = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", post.title)
    check_description = re.fullmatch(r"([-A-Za-z0-9!?#()' .,_]+)", post.description)
    if check_title and check_description:
        new_post = Post(
            title=post.title,
            description=post.description,
            author=current_user.username,
            publication_date=datetime.utcnow(),
        )
        await dao.add_new_post(new_post)
        await dao.commit()
        await dao.refresh_new_post(new_post)
        return dto.MainPost(
            id=new_post.id,
            title=new_post.title,
            description=new_post.description,
            author=new_post.author,
            publication_date=new_post.publication_date,
            likes=None
        )
    else:
        raise InaccessibleCharactersException


async def get_posts_all(dao: AllPostsGetter) -> List[dto.MainPost]:
    return await dao.get_all_posts()


async def get_by_id_post(post_id: int, dao: PostByIDGetter):
    return await dao.get_post_with_comments_by_id(post_id)


async def return_post_by_id(post, comments, dao: PostByIDReturner) -> dto.MainRetrievePost:
    return await dao.return_post_by_id(post, comments)


async def get_posts_query_search(search: str, dao: PostsByQuerySearchGetter) -> List[dto.MainPost]:
    return await dao.get_post_by_query_search(search)


async def get_my_post_list(username: str, dao: MyPostsGetter) -> List[dto.MainPost]:
    return await dao.get_my_posts(username)


async def post_update(post: dto.UpdatePost, post_id: int,
                      dao: PostUpdater, username: str) -> str:
    return await dao.update_post(post, post_id, username)


async def post_delete(post_id: int, username: str, dao: PostDeleter) -> str:
    return await dao.delete_post(post_id, username)


async def posts_by_user(author: str, dao: PostByUserGetter) -> List[dto.MainPost]:
    return await dao.user_posts(author)


async def get_simple_post_by_id(post_id: int, dao: SimplePostGetter) -> dto.MainPost:
    return await dao.get_post_by_id(post_id)


async def check_post_existence(post_id: int, dao: PostExistenceChecker) -> None:
    return await dao.check_post_existence(post_id)

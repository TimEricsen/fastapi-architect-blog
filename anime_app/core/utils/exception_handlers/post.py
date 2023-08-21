from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.post import PostIDNotFoundException, NotPositivePostIDException, \
    PostNotFoundOrNotCreatorException, PostOrCommentNotFoundException, NotPostOwnerException, EmptyPostListException


async def post_id_not_found_handler(request: Request, exc: PostIDNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': f'Post with id {exc.post_id} not found!'}
    )


async def not_positive_post_id_handler(request: Request, exc: NotPositivePostIDException):
    return JSONResponse(
        status_code=400,
        content={'message': 'Id should be a positive numeric value!'}
    )


async def post_or_comment_not_found_handler(request: Request, exc: PostOrCommentNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': 'Post or Comment not found!'}
    )


async def not_post_owner_handler(request: Request, exc: NotPostOwnerException):
    return JSONResponse(
        status_code=400,
        content={'message': 'You cannot delete comment cause you are not owner of this post!'}
    )


async def empty_post_list_handler(request: Request, exc: EmptyPostListException):
    return JSONResponse(
        status_code=404,
        content={'message': 'Posts not found!'}
    )


async def post_not_found_or_not_creator_handler(request: Request, exc: PostNotFoundOrNotCreatorException):
    return JSONResponse(
        status_code=403,
        content={'message': 'Post with this id not found, or you are not owner of this post!'}
    )

from fastapi import Request
from fastapi.responses import JSONResponse

from anime_app.core.utils.exceptions.comment import CommentsNotFoundException, CommentNotFoundOrNotCreatorException


async def comment_not_found_or_not_creator_handler(request: Request, exc: CommentNotFoundOrNotCreatorException):
    return JSONResponse(
        status_code=403,
        content={'message': 'Comment not found or you are not a creator of it!'}
    )


async def comments_not_found_handler(request: Request, exc: CommentsNotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': 'You have not commented any post yet!'}
    )

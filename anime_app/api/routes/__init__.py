from fastapi import FastAPI

from anime_app.api.routes import black_list, comment, comment_like, complaint, \
    complaint_comment, favourites, like, post, user


def setup_routers(app: FastAPI):
    app.include_router(user.router)
    app.include_router(post.router)
    app.include_router(comment.router)
    app.include_router(like.router)
    app.include_router(comment_like.router)
    app.include_router(complaint.router)
    app.include_router(complaint_comment.router)
    app.include_router(favourites.router)
    app.include_router(black_list.router)

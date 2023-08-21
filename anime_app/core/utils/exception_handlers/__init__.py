from fastapi import FastAPI

from anime_app.core.utils.exceptions.base import InaccessibleCharactersException
from anime_app.core.utils.exceptions.black_list import SelfAddToBLException, UserAlreadyInBLException, \
    UserNotInBLException, UserInBLException, EmptyBLException
from anime_app.core.utils.exceptions.comment import CommentsNotFoundException, CommentNotFoundOrNotCreatorException
from anime_app.core.utils.exceptions.complaint import SelfComplaintException, AlreadyComplainedException
from anime_app.core.utils.exceptions.favourites import PostAlreadyInFavouritesException, PostNotInFavouritesException
from anime_app.core.utils.exceptions.like import LikesNotFoundException
from anime_app.core.utils.exceptions.post import PostIDNotFoundException, PostOrCommentNotFoundException, \
    PostNotFoundOrNotCreatorException, NotPostOwnerException, NotPositivePostIDException, EmptyPostListException
from anime_app.core.utils.exceptions.user import UserIDNotFoundException, IncorrectUsernameOrPasswordException, \
    UsernameAlreadyExistsException, EmailAlreadyExistsException, CredentialException, PasswordMismatch

from anime_app.core.utils.exception_handlers.base import inaccessible_characters_handler
from anime_app.core.utils.exception_handlers.black_list import self_add_to_bl_handler, user_in_bl_handler, \
    user_already_in_bl_handler, user_not_in_bl_handler, empty_bl_handler
from anime_app.core.utils.exception_handlers.comment import comments_not_found_handler, \
    comment_not_found_or_not_creator_handler
from anime_app.core.utils.exception_handlers.complaint import already_complained_handler, self_complaint_handler
from anime_app.core.utils.exception_handlers.favourites import post_in_favourites_handler, post_not_in_fav_handler
from anime_app.core.utils.exception_handlers.like import like_not_found_handler
from anime_app.core.utils.exception_handlers.post import post_id_not_found_handler, empty_post_list_handler, \
    not_post_owner_handler, not_positive_post_id_handler, post_not_found_or_not_creator_handler, \
    post_or_comment_not_found_handler
from anime_app.core.utils.exception_handlers.user import user_id_not_found_handler, username_exists_handler, \
    email_exists_handler, incorrect_username_or_password_handler, password_mismatch, credential_exception


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(InaccessibleCharactersException, inaccessible_characters_handler)

    app.add_exception_handler(SelfAddToBLException, self_add_to_bl_handler)
    app.add_exception_handler(UserAlreadyInBLException, user_already_in_bl_handler)
    app.add_exception_handler(UserInBLException, user_in_bl_handler)
    app.add_exception_handler(UserNotInBLException, user_not_in_bl_handler)
    app.add_exception_handler(EmptyBLException, empty_bl_handler)

    app.add_exception_handler(CommentNotFoundOrNotCreatorException, comment_not_found_or_not_creator_handler)
    app.add_exception_handler(CommentsNotFoundException, comments_not_found_handler)

    app.add_exception_handler(SelfComplaintException, self_complaint_handler)
    app.add_exception_handler(AlreadyComplainedException, already_complained_handler)

    app.add_exception_handler(PostAlreadyInFavouritesException, post_in_favourites_handler)
    app.add_exception_handler(PostNotInFavouritesException, post_not_in_fav_handler)

    app.add_exception_handler(LikesNotFoundException, like_not_found_handler)

    app.add_exception_handler(PostIDNotFoundException, post_id_not_found_handler)
    app.add_exception_handler(PostOrCommentNotFoundException, post_or_comment_not_found_handler)
    app.add_exception_handler(PostNotFoundOrNotCreatorException, post_not_found_or_not_creator_handler)
    app.add_exception_handler(NotPostOwnerException, not_post_owner_handler)
    app.add_exception_handler(NotPositivePostIDException, not_positive_post_id_handler)
    app.add_exception_handler(EmptyPostListException, empty_post_list_handler)

    app.add_exception_handler(UserIDNotFoundException, user_id_not_found_handler)
    app.add_exception_handler(IncorrectUsernameOrPasswordException, incorrect_username_or_password_handler)
    app.add_exception_handler(PasswordMismatch, password_mismatch)
    app.add_exception_handler(CredentialException, credential_exception)
    app.add_exception_handler(UsernameAlreadyExistsException, username_exists_handler)
    app.add_exception_handler(EmailAlreadyExistsException, email_exists_handler)

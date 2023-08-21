import pytest


@pytest.mark.asyncio
async def test_create_get_delete_post(
    post_data,
    comment_data,
    user_data,
    create_database_models,
    delete_database_models,
    get_post_from_database,
    get_comment_from_database,
    get_user_from_database
):
    await create_database_models()
    post = await get_post_from_database(1)
    comment = await get_comment_from_database(1)
    user = await get_user_from_database(1)
    assert post.title == 'What about this title?'
    assert comment.text == 'My commeeeent'
    assert comment.post_id == 1
    assert user.username == 'Someone'

    await delete_database_models()

    post2 = await get_post_from_database(comment.id)
    comment2 = await get_comment_from_database(post.id)
    user2 = await get_user_from_database(user.id)
    assert post2 is None
    assert comment2 is None
    assert user2 is None

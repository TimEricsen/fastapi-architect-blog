import pytest

from httpx import AsyncClient

from anime_app.core.models import dto


@pytest.mark.asyncio
async def test_my_comments(client: AsyncClient, get_comment_from_database,
                           create_database_models, delete_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.get(
        '/user/me/comments',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()
    comment = await get_comment_from_database(1)
    dto_comment = dto.MainComment(
        text=comment.text,
        author=comment.author,
        time_posted=comment.time_posted,
        post_id=1,
        likes=0
    )
    comment = dto_comment.dict()
    comment['time_posted'] = comment['time_posted'].strftime('%Y-%m-%dT%H:%M:%S.%f')
    assert response.json() == [comment]
    await delete_database_models()

import pytest

from httpx import AsyncClient

from anime_app.core.models import dto


@pytest.mark.asyncio
async def test_get_post_from_db(client: AsyncClient, user_data,
                                get_post_from_database, create_database_models):
    await create_database_models()
    response = await client.get(
        '/posts/post/1'
    )
    response.read()

    post = await get_post_from_database(response.json()['id'])

    assert response.is_success
    assert response.json()['title'] == post.title
    assert response.json()['author'] == user_data['username']


@pytest.mark.asyncio
async def test_get_post_false(client: AsyncClient):
    response = await client.get(
        '/posts/post/3'
    )
    response.read()
    assert response.json()['message'] == 'Post with id 3 not found!'

    response = await client.get(
        '/posts/post/-4'
    )
    response.read()
    assert response.json()['message'] == 'Id should be a positive numeric value!'


@pytest.mark.asyncio
async def test_get_my_posts(client: AsyncClient, get_post_from_database, delete_database_models):
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.get(
        '/posts/my',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()
    post = await get_post_from_database(1)
    dto_post = dto.MainPost(
        id=post.id,
        title=post.title,
        description=post.description,
        author=post.author,
        publication_date=post.publication_date,
        likes=0
    )
    post = dto_post.dict()
    post['publication_date'] = post['publication_date'].strftime('%Y-%m-%dT%H:%M:%S.%f')

    assert response.json() == [post]
    await delete_database_models()

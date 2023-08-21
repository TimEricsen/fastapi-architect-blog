import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_like_to_post(client: AsyncClient, create_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()

    token = response.json()['access_token']

    response = await client.get(
        '/posts/post/1/like',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'Your like has been added!'


@pytest.mark.asyncio
async def test_like_to_comment(client: AsyncClient, delete_database_models):
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()

    token = response.json()['access_token']

    response = await client.get(
        '/posts/post/1/comment/1/like',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'Your like has been added!'

    await delete_database_models()

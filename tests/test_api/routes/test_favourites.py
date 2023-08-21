import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_post_to_favourites(client: AsyncClient, create_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.get(
        '/posts/post/1/add-to-favourites',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'Added to favourites!'


@pytest.mark.asyncio
async def test_delete_post_from_favourites(client: AsyncClient, delete_database_models):
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.delete(
        '/posts/post/1/delete-from-favourites',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'Post deleted from favourites!'

    await delete_database_models()

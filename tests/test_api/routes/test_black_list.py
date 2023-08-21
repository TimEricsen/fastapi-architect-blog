import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_to_bl(client: AsyncClient, create_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.get(
        '/add-to-black-list/2',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'You added user with id 2 to black list'


@pytest.mark.asyncio
async def test_delete_from_bl(client: AsyncClient, delete_database_models):
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.delete(
        '/delete-from-black-list/2',
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'You removed this user from black list!'

    await delete_database_models()

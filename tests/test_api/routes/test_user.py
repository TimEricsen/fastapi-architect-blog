import json

import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_auth(client: AsyncClient, get_user_from_database, create_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    assert response.is_success
    response.read()
    token = response.json()['access_token']

    response = await client.get(
        '/user/me',
        headers={'Authorization': 'Bearer ' + token},
        follow_redirects=True
    )
    assert response.is_success

    response.read()
    user = await get_user_from_database(response.json()['id'])
    assert user.username == response.json()['username']


@pytest.mark.asyncio
async def test_user_register_false(client: AsyncClient, delete_database_models):
    request = {
        'username': 'Someone',
        'email': 'someoneemail@gmail.com',
        'password': 'password',
        'repeat_password': 'password'
    }
    response = await client.post(
        '/user/registration',
        data=json.dumps(request)
    )

    response.read()
    assert response.is_error
    assert response.json()['message'] == 'This username is already used!'
    await delete_database_models()

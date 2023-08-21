import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_complaint_to_post(client: AsyncClient, create_database_models):
    await create_database_models()
    response = await client.post(
        '/user/token',
        data={'username': 'SecondOne', 'password': 'password2'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.post(
        '/posts/post/1/complaint',
        json={'reason': 'Spam'},
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_success
    assert response.json() == 'Thanks for the help! We will definitely look into your complaint!'


@pytest.mark.asyncio
async def test_complaint_to_post_false(client: AsyncClient):
    response = await client.post(
        '/user/token',
        data={'username': 'SecondOne', 'password': 'password2'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.post(
        '/posts/post/1/complaint',
        json={'reason': 'Sapm'},
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_error
    assert response.json()['detail'][0]['msg'] == "value is not a valid enumeration member; permitted: " \
                                                  "'Discriminatory speech or slander', 'Spam'," \
                                                  " 'Advertising of illegal content'"


@pytest.mark.asyncio
async def test_complaint_own_post(client: AsyncClient, delete_database_models):
    response = await client.post(
        '/user/token',
        data={'username': 'Someone', 'password': 'password'}
    )
    response.read()
    token = response.json()['access_token']

    response = await client.post(
        '/posts/post/1/complaint',
        json={'reason': 'Spam'},
        headers={'Authorization': 'Bearer ' + token}
    )
    response.read()

    assert response.is_error
    assert response.json()['message'] == 'You cannot complain about own content!'

    await delete_database_models()

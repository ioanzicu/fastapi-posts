import pytest
from jose import jwt
from fastapi import status
from app import schemas
from app.config import settings
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {'email': 'thebest-alpaca@mail.com', 'password': 'alpaca1234'}
    responses = client.post('/users/', json=user_data)
    assert responses.status_code == status.HTTP_201_CREATED
    new_user = responses.json()
    new_user['password'] = user_data['password']
    return new_user


def test_root(client):
    response = client.get('/')
    assert response.json().get(
        'message') == 'Hi, I see that a good man is visiting us. I am glad that you opened this app. Wish you a good day! ;)'
    assert response.status_code == status.HTTP_200_OK


def test_create_user(client):
    response = client.post(
        '/users/', json={'email': 'thebest-alpaca@mail.com', 'password': 'alpaca1234'})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == 'thebest-alpaca@mail.com'
    assert response.status_code == status.HTTP_201_CREATED


def test_login_user(client, test_user):
    response = client.post(
        '/login', data={'username': test_user.get('email'), 'password': test_user.get('password')})
    login_response = schemas.Token(**response.json())

    payload = jwt.decode(login_response.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id: str = payload.get('user_id')

    assert id == test_user.get('id')
    assert login_response.token_type == 'bearer'
    assert response.status_code == status.HTTP_200_OK

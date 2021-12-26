import pytest
from jose import jwt
from fastapi import status
from app import schemas
from app.config import settings


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


@pytest.mark.parametrize('email, password, status_code, detail', [
    ('WrongEmail@gmail.com', 'alpaca1234',
     status.HTTP_403_FORBIDDEN, 'Invalid Credentials'),
    ('thebest-alpaca@mail.com', 'wrong_PassworD',
     status.HTTP_403_FORBIDDEN, 'Invalid Credentials'),
    ('WrongEmail@gmail.com', 'wrong_PassworD',
     status.HTTP_403_FORBIDDEN, 'Invalid Credentials'),
    (None, 'wrong_PassworD', 422, [{'loc': [
     'body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}]),
    ('thebest-alpaca@mail.com', None, 422,
     [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}])
])
def test_incorrect_login(client, test_user, email, password, status_code, detail):
    response = client.post(
        '/login', data={'username': email, 'password': password})

    assert response.status_code == status_code
    assert response.json().get('detail') == detail

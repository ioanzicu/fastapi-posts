from fastapi import status
from app import schemas
from .database import client, session


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

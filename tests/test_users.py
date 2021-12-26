from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.json().get('message') == 'Hi, I see that a good man is visiting us. I am glad that you opened this app. Wish you a good day! ;)'
    assert response.status_code == status.HTTP_200_OK



def test_create_user():
    response = client.post('/users/', json={'email': 'thebest-alpaca@mail.com', 'password': 'alpaca1234'})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == 'thebest-alpaca@mail.com'
    assert response.status_code == status.HTTP_201_CREATED


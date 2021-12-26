from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
import pytest


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# runs before each test
@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)  # drop tables
    # set up - run out code before we run our test
    Base.metadata.create_all(bind=engine)  # create tables
    yield TestClient(app)
    # cleanup - run our test after our test finished

    # OR
    # Base.metadata.create_all(bind=engine) # create tables
    # yield TestClient(app)
    # Base.metadata.drop_all(bind=engine)  # drop tables

    # OR - alembic
    # command.upgrade('head')
    # yield TestClient(app)
    # command.downgrade('base')


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

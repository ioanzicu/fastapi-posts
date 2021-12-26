# all fixtures from this file will be available into the tests folder without imports
import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from fastapi import status


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)  # drop tables
    Base.metadata.create_all(bind=engine)  # create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# runs before each test
@pytest.fixture(scope='function')
def client(session):  # will run after session fixture
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': 'thebest-alpaca@mail.com', 'password': 'alpaca1234'}
    responses = client.post('/users/', json=user_data)
    assert responses.status_code == status.HTTP_201_CREATED
    new_user = responses.json()
    new_user['password'] = user_data['password']
    return new_user

from fastapi.testclient import TestClient
import pytest
from fastapi import Depends
from app.main import app
from app import schemas
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    from app.config import settings

    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{settings.database_username}:"
        f"{settings.database_password}@"
        f"{settings.database_hostname}:"
        f"{settings.database_port}/"
        f"{settings.database_name}_test"
    )

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg2://",
        1
    )

engine = create_engine(DATABASE_URL)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# client =TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    # run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after our test finishes

@pytest.fixture
def create_user(client):
    user_data = {
            "email" : "sathish123@gmail.com",
            "password" : "password123"
        }
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    print(res.json())
    print(new_user)
    assert res.status_code == 201
    return new_user

@pytest.fixture
def token(create_user):
    return create_access_token({"user_id" : create_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(create_user, session):
    test_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": create_user["id"]
        },
        {
            "title": "Second title",
            "content": "Second content",
            "owner_id": create_user["id"]
        },
        {
            "title": "Third title",
            "content": "Third content",
            "owner_id": create_user["id"]
        },
    ]

    def create_test_post(post):
        return models.Post(**post)

    post_map = map(create_test_post, test_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()

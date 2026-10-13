from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db, Base


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

app.dependency_overrides[get_db] = override_get_db

# client =TestClient(app)

@pytest.fixture()
def client():
    # run our code before we run our test
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    yield TestClient(app)
    # run our code after our test finishes

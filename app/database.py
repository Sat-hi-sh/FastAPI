from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings


database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,
)

engine = create_engine(database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", password = "Developer@24", cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Database has been connected Successfully")
#         break

#     except Exception as error:
#         print("Database Connectivity Failed")
#         print("Error :", error)
#         time.sleep(2)
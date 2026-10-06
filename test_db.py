import os
from sqlalchemy import create_engine

url = os.environ["DATABASE_URL"]

if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql+psycopg2://", 1)

print("Testing database connection...")

engine = create_engine(url)

try:
    with engine.connect() as connection:
        print("DATABASE CONNECTION SUCCESS")
except Exception as e:
    print("DATABASE CONNECTION FAILED")
    print(type(e).__name__)
    print(e)
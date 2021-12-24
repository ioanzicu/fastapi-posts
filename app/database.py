import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='postgres',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesfull!!!')
#         break
#     except Exception as exc:
#         print('Connection to database failed!')
#         print(exc)
#         time.sleep(2)

# https://fastapi.tiangolo.com/
# https://www.sqlalchemy.org/

import psycopg2
import time
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfull!!!')
        break
    except Exception as exc:
        print('Connection to database failed!')
        print(exc)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
async def root():
    return {'message': 'Hello Fast Py!!!'}

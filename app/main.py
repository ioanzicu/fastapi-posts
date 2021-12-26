# https://fastapi.tiangolo.com/
# https://www.sqlalchemy.org/
# https://alembic.sqlalchemy.org/en/latest/


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote

# Needed for sqlalchemy but not needed for alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']  # in production - only the domains that SHOULD have access

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def root():
    return {'message': 'Hi, I see that a good man is visiting us. I am glad that you opened this app. Wish you a good day! ;)'}

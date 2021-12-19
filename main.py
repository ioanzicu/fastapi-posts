# https://fastapi.tiangolo.com/
# https://pydantic-docs.helpmanual.io/

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

from pydantic.typing import NONE_TYPES

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{'id': 1, 'title': 't1', 'content': 'c1'},
            {'id': 2, 'title': 't2', 'content': 'c2'},
            {'id': 3, 'title': 't3', 'content': 'c3'}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def get_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


def remove_from_array(index):
    my_posts.pop(index)


@app.get('/')
async def root():
    return {'message': 'Hello Fast Py!!!'}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(type(post), post)
    print(type(post.dict()), post.dict())

    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {'data': post_dict}


@app.get('/posts/latest')
def get_lastest_post():
    lastest_post = my_posts[-1]
    return {'lastest_post': lastest_post}


#  order matters
@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    id = int(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found!')
    return {'post': find_post(id)}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    print('id', type(id), id)
    id = int(id)
    index = get_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, post: Post):
    index = get_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return Response(status_code=status.HTTP_204_NO_CONTENT)

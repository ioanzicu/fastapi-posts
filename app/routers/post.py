from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import models
from ..database import get_db
from ..schemas import PostCreate, Post
from typing import List

router = APIRouter()


@router.get('/posts', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    post = models.Posts(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/posts/{id}', response_model=Post)
def get_post(id: int,  db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found!')
    return post


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/posts/{id}', response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

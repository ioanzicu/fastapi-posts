
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from .. import models
from ..database import get_db
from ..schemas import UserCreate, UserOut

router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Hash the password - and store in user.password
    hashed_password = hash(user.password)
    user.password = hashed_password

    user_exists = db.query(models.User).filter(models.User.email == user.email)
    if user_exists.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'User with email {user.email} already exists')

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} does not exist')
    return user

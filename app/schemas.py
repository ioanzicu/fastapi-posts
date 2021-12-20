# https://pydantic-docs.helpmanual.io/
from pydantic import BaseModel

# request schema


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

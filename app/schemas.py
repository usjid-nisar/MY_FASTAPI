from pydantic import BaseModel, conint,EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
   
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type: ignore

class Config:
    env_file = ".env"

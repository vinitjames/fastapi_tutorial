from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    published: bool = True

class PostUpdate(PostBase):
    published: bool = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserAuthToken(BaseModel):
    access_token: str
    token_type: str

class UserAuthTokenData(BaseModel):
    user_id: str
    exp: Optional[datetime] = None

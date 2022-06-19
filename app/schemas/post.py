from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from .user import UserData

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
    owner: UserData
    
    class Config:
        orm_mode = True

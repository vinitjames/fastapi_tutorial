from pydantic import BaseModel
from datetime import datetime

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

    

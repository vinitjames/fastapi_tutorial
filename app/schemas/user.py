from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

    
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

class UserData(BaseModel):
    id: str
    email: EmailStr
    class Config:
        orm_mode = True


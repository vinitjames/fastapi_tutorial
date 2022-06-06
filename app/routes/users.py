from fastapi import HTTPException, status, Response, Depends, APIRouter
from typing import List
from .. import models, schemas, crypto
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users",
                   tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)) -> dict:
  user.password = crypto.hash(user.password)
  new_user = models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_users(id: int, db: Session=Depends(get_db)) -> dict:
  user = db.query(models.User).filter(models.User.id == id).first()
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with id: {id} was not found")
    
  return user

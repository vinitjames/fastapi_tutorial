from fastapi import HTTPException, status, Response, Depends, APIRouter
from typing import List
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/post",
                   tags=["Posts"] )


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db)) -> dict:
  posts = db.query(models.Post).all()
  return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session=Depends(get_db)) -> dict:
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)) -> dict:
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.update(post.dict(), synchronize_session=False)
  db.commit() 
  return post_query.first()

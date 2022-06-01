from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, List
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
  return "Hello this is fast api tutorial"


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db)) -> dict:
  posts = db.query(models.Post).all()
  return posts

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session=Depends(get_db)) -> dict:
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)) -> dict:
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  

@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.update(post.dict(), synchronize_session=False)
  db.commit() 
  return post_query.first()
  
  

from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.base.metadata.create_all(bind=engine)

app = FastAPI()
  

class Post(BaseModel):
  title: str
  content: str
  published: bool = True  


@app.get("/")
def root():
  return "Hello this is fast api tutorial"


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)) -> dict:
  posts = db.query(models.Post).all()
  return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int, db: Session=Depends(get_db)) -> dict:
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return {"post_detail" : post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session=Depends(get_db)) -> dict:
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return {"data" : new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session=Depends(get_db)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  if(post_query.first() == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_query.update(post.dict(), synchronize_session=False)
  db.commit() 
  return {"data": post_query.first()}
  
  

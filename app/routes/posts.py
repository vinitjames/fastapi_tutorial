from fastapi import HTTPException, status, Response, Depends, APIRouter
from typing import List
from .. import models, oauth2
from ..database import get_db
from ..schemas.post import PostResp, PostWithVoteResp, PostCreate, PostUpdate
from ..schemas.user import UserData
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts",
                   tags=["Posts"] )


@router.get("/", response_model=List[PostWithVoteResp])
def get_posts(db: Session=Depends(get_db),
              current_user: UserData = Depends(oauth2.get_current_user),
              limit: int=10, skip: int=0, search: str="") -> dict:
  posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True
  ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
  return posts

@router.get("/{id}", response_model=PostWithVoteResp)
def get_post(id: int, db: Session=Depends(get_db),
             current_user: UserData = Depends(oauth2.get_current_user)) -> dict:
  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True
  ).group_by(models.Post.id).filter(models.Post.id == id).first()
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResp)
def create_posts(post: PostCreate, db: Session=Depends(get_db),
                 current_user: UserData = Depends(oauth2.get_current_user)) -> dict:
  new_post = models.Post(owner_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db),
                current_user: UserData = Depends(oauth2.get_current_user)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if(post == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  if(post.owner_id != current_user.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not Authorized to perform given operation")
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  
@router.put("/{id}", response_model=PostResp)
def update_post(id: int, updated_post: PostUpdate, db: Session=Depends(get_db),
                current_user: UserData = Depends(oauth2.get_current_user)) -> dict:
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if(post == None):  
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  if(post.owner_id != current_user.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not Authorized to perform given operation")
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit() 
  return post_query.first()

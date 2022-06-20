from fastapi import HTTPException, status, Response, Depends, APIRouter
from ..schemas.vote import Vote
from ..database import get_db
from .. import oauth2, models
from ..schemas.user import UserData
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes",
                   tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session=Depends(get_db),
         current_user: UserData=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} not found")
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    vote_entry = vote_query.first()
    
    if (not vote_entry) and (vote.dir == 0):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has not liked  post {vote.post_id}')
    elif (vote_entry) and (vote.dir == 1):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} already voted on post {vote.post_id}')
        
    elif (not vote_entry) and (vote.dir == 1):
        db.add(models.Vote(user_id=current_user.id, post_id=vote.post_id))
        return_msg = "vote succsessfully added for the post"
       
    else:
        vote_query.delete(synchronize_session=False)
        return_msg = "vote succsessfully removed for the post"
        
    db.commit()
    return {"status_message": return_msg}
    
            

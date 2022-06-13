from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, database, crypto, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.UserAuthToken)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invaild user credentials")
    if not crypto.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invaild user credentials")
    access_token = oauth2.create_access_token(data = schemas.UserAuthTokenData(user_id = user.id))
    oauth2.verify_access_token(access_token, HTTPException(status_code=status.HTTP_401_UNAUTHORIZED))
    return {"access_token":access_token, "token_type":"bearer"}












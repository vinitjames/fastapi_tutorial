from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, database, crypto, oauth2
from ..schemas.user import UserAuthTokenData, UserAuthToken


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=UserAuthToken)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invaild user credentials")
    if not crypto.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invaild user credentials")
    access_token = oauth2.create_access_token(data = UserAuthTokenData(user_id = user.id))
    return {"access_token":access_token, "token_type":"bearer"}












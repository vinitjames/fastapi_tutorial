from jose import JWTError, jwt
from typing import Union, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from .schemas.user import UserAuthTokenData, UserData
from .database import get_db
from .config import oauth2_config 

SECRET_KEY = oauth2_config.JWT_secret_key
ALGORITHM = oauth2_config.JWT_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = oauth2_config.JWT_timeout

oauth2_schema = OAuth2PasswordBearer(tokenUrl= 'login')

def create_access_token(data: UserAuthTokenData, expire_delta: Union[timedelta, None] = None) -> str:
    if expire_delta:
        data.exp = datetime.utcnow() + expire_delta
    else:
        data.exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)



def verify_access_token(token: str, credentials_exception: Exception) -> UserAuthTokenData:
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = UserAuthTokenData(**decoded_data)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_schema), db: Session = Depends(get_db)) -> UserData:
    access_token_data = verify_access_token(token,
                                            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                          detail=f"Could not validate credentials",
                                                          headers={"WWW-Authenticate": "Bearer"}))
    user = db.query(models.User).filter(models.User.id == access_token_data.user_id).first()
    return user



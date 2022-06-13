from jose import JWTError, jwt
from typing import Union, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from . import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl= 'login')

def create_access_token(data: schemas.UserAuthTokenData, expire_delta: Union[timedelta, None] = None) -> str:
    if expire_delta:
        data.exp = datetime.utcnow() + expire_delta
    else:
        data.exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)



def verify_access_token(token: str, credentials_exception: Exception) -> schemas.UserAuthTokenData:
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = schemas.UserAuthTokenData(**decoded_data)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_schema)) -> schemas.UserAuthTokenData:
    return verify_access_token(token, HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                    details=f"Could not validate credentials",
                                                    headers={"WWW-Authenticate": "Bearer"}))




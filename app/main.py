from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, List
from . import models, schemas, crypto
from .database import engine, get_db
from .routes import posts, users, auth
from sqlalchemy.orm import Session


models.base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
  return "Hello this is fast api tutorial"



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routes import posts, users, auth, votes
from .database import engine



#models.base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def root():
  return "Hello this is fast api tutorial"



from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  required: bool = True
  rating: Optional[int] = None
  
post_cache = [{"title": "this is 1st post", "content": "this is a shit post", "id":1},
              {"title": "this is 2nd post", "content": "this is a shit post too", "id":2}]

def find_post(id: int) -> dict:
  for post in post_cache:
    if post["id"] == id:
      return post
  return None

def get_index(id: int) -> Optional[int]:
  for index, post in enumerate(post_cache):
    if post["id"] == id :
      return index
  return None

@app.get("/")
def root():
  return "Hello this is fast api tutorial"


@app.get("/posts")
def get_posts() -> dict:
  return {"data": post_cache}

@app.get("/posts/{id}")
def get_post(id: int) -> dict:
  post = find_post(id)
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return {"post_detail" : post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post) -> dict:
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    post_cache.append(post_dict)
    return {"data" : post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> dict:
  index = get_index(id)
  if(index == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_cache.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  

@app.put("/posts/{id}")
def update_post(id: int, post: Post) -> dict:
  index = get_index(id)
  if(index == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  post_dict = post.dict()
  post_dict["id"] = id
  post_cache[index] = post_dict
  return {"data":post_dict}
  
  

from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow

app = FastAPI()

while True:
  try:
    conn = psycopg2.connect(database='fastapi_test', user='postgres',
                            cursor_factory= RealDictCursor)
    cursor = conn.cursor() 
    print("database connected")
    break
  
  except Exception as error:
    print(error)
    time.sleep(5)

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
  cursor.execute(""" SELECT * FROM posts """)
  posts = cursor.fetchall()
  return {"data": posts}

@app.get("/posts/{id}")
def get_post(id: int) -> dict:
  cursor.execute(""" SELECT * FROM posts where id = %s """, str(id))
  post = cursor.fetchone()
  if(post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return {"post_detail" : post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post) -> dict:
  cursor.execute(""" INSERT INTO posts (title, content, required)  
                     VALUES (%s, %s, %s) RETURNING * """,
                 (post.title, post.content, post.required))
  new_post = cursor.fetchone()
  conn.commit()
  return {"data" : new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int) -> dict:
  cursor.execute(""" DELETE FROM posts WHERE id = %s  
                     RETURNING * """, (str(id),))
  deleted_post = cursor.fetchone()
  conn.commit()
  if(deleted_post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  return Response(status_code=status.HTTP_204_NO_CONTENT) 
  

@app.put("/posts/{id}")
def update_post(id: int, post: Post) -> dict:
  cursor.execute(""" UPDATE posts SET title = %s, content = %s, required = %s WHERE id = %s 
                     RETURNING * """, (post.title, post.content, post.required, str(id)))
  updated_post = cursor.fetchone()
  conn.commit()
  if(updated_post == None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  return {"data": updated_post}
  
  

from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='fastapi',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("connection succeded")
except Exception as error:
    print("Connection Failed")
    print(error)


my_posts = [{"title":"Title of Post 1" , "content":"Content of Post 1" , "id":1},
            {"title":"fav food" , "content":"pizza" , "id":2}]


def findPostIndex(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

def findPost(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None
        

@app.get("/my-posts")
async def root():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return posts

@app.post("/new-post")
def createNewPost(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) 
                   RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    return {"data":new_post} 

@app.get("/get-post/{id}")
def getPostById (id: int ):
    print(id)
    post  = findPost(id)
    if not  post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    return {"data": post}


@app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePostById(id: int):
    post_index = findPostIndex(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    my_posts.pop(post_index)
    return {"message": f"Deleted post with id {id}"}


@app.put("/update-post/{id}")
def updatePostById(id : int, newPost: Post):
    post = findPost(id)
    if  post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    post.update(newPost)
    return {"message": post}

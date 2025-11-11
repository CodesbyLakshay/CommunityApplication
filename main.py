from typing import Optional
from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: Optional[str] = None


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
    return my_posts

@app.post("/new-post")
def createNewPost(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange (0,1000000)
    my_posts.append(post_dict )
    print(my_posts)
    return post_dict

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

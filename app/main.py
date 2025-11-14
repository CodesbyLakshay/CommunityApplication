from contextlib import asynccontextmanager

import psycopg2
from fastapi import FastAPI , Response , status , HTTPException
from .models import Post
from .database import engine, create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)



# my_posts = [{"title":"Title of Post 1" , "content":"Content of Post 1" , "id":1},
#             {"title":"fav food" , "content":"pizza" , "id":2}]
#
#
# def findPostIndex(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#     return None
#
# def findPost(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
#     return None
#
#
# @app.get("/my-posts")
# async def root():
#     #cursor.execute(""" SELECT * FROM posts """)
#    # posts = cursor.fetchall()
#     #return posts
#
# @app.post("/new-post")
# def createNewPost(post: Post):
#     cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)
#                    RETURNING * """,(post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}
#
# @app.get("/get-post/{id}")
# def getPostById (id: int ):
#     print(id)
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(id,))
#     post  = cursor.fetchone()
#     if not  post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
#     return {"data": post}
#
#
# @app.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def deletePostById(id: int):
#    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
#    post = cursor.fetchone()
#    conn.commit()
#    if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
#
#    return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
# @app.put("/update-post/{id}")
# def updatePostById(id : int, newPost: Post):
#     cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """,(newPost.title,newPost.content,newPost.published,id))
#     post = cursor.fetchone()
#     conn.commit()
#     if  post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
#     return {"message": post}

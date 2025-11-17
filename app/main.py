from contextlib import asynccontextmanager

from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .database import  create_db, get_async_session
from . import models, schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/my-posts")
async def root( session:AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return {"posts":posts}


@app.post("/new-post")
async def create_new_post(
    post: schemas.PostCreate,session: AsyncSession = Depends(get_async_session)):
    new_post = models.Post(title=post.title, content=post.content)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return schemas.PostResponse.model_validate(new_post)


@app.get("/get-post/{id}")
async def getPostbyId(id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    return {"post":post}


@app.put("/update-post/{id}")
async def updatePostById(updated_post: schemas.PostCreate ,id: int , session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    post.title = updated_post.title
    post.content = updated_post.content
    await session.commit()
    await session.refresh(post)
    return schemas.PostResponse.model_validate(post)

@app.delete("/delete-post/{id}",status_code=204)
async def deletePostById(id: int , sessions: AsyncSession = Depends(get_async_session)):
    result = await sessions.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    await sessions.delete(post)
    await sessions.commit()
    return {"deleted":True}


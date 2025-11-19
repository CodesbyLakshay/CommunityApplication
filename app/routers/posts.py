from .. import models, schemas, oauth2
from fastapi import Depends, FastAPI, HTTPException , status ,Response ,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_async_session
from ..models import Post
from typing import List

router = APIRouter()

@router.get("/all-posts", response_model=List[schemas.PostResponse])
async def root( session:AsyncSession = Depends(get_async_session), user_id : str = Depends(oauth2.get_current_user)):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts


@router.post("/new-post" , response_model=schemas.PostResponse)
async def create_new_post(
    post: schemas.PostCreate,session: AsyncSession = Depends(get_async_session), user_id : str = Depends(oauth2.get_current_user)):
    print(user_id)
    new_post = models.Post(title=post.title, content=post.content)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@router.get("/get-post/{id}",response_model=schemas.PostResponse)
async def getPostbyId(id: int, session: AsyncSession = Depends(get_async_session),user_id : str = Depends(oauth2.get_current_user)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    return post


@router.put("/update-post/{id}",response_model=schemas.PostResponse)
async def updatePostById(updated_post: schemas.PostCreate ,id: int , session: AsyncSession = Depends(get_async_session),user_id : str = Depends(oauth2.get_current_user)):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    post.title = updated_post.title
    post.content = updated_post.content
    await session.commit()
    await session.refresh(post)
    return post

@router.delete("/delete-post/{id}",status_code=204)
async def deletePostById(id: int , sessions: AsyncSession = Depends(get_async_session),user_id : str = Depends(oauth2.get_current_user)):
    result = await sessions.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    await sessions.delete(post)
    await sessions.commit()
    return {"deleted":True}








from .. import models, schemas, oauth2
from fastapi import Depends, HTTPException  ,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select , func
from ..database import get_async_session
from ..models import Post ,Vote
from typing import List, Optional

router = APIRouter()

@router.get("/all-posts",response_model=List[schemas.PostVoteResponse])
async def root( session: AsyncSession = Depends(get_async_session), user_id : str = Depends(oauth2.get_current_user),limit:int = 10 , skip:int = 0,search:Optional[str] = ""):

    votes= (await session.execute(select(Post,func.count(Vote.post_id).label("votes")).outerjoin(Vote,Post.id == Vote.post_id).filter(Post.title.contains(search)).limit(limit).offset(skip).group_by(Post.id))).mappings().all()
    return votes


@router.post("/new-post" , response_model=schemas.PostResponse)
async def create_new_post(
    post: schemas.PostCreate,session: AsyncSession = Depends(get_async_session), id : str = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=post.title, content=post.content , user_id=int(id.id))
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


@router.get("/get-post/{id}",response_model=schemas.PostVoteResponse)
async def getPostbyId(id: int, session: AsyncSession = Depends(get_async_session),user_id : str = Depends(oauth2.get_current_user)):
    post = (await session.execute(select(Post,func.count(Vote.post_id).label("votes")).outerjoin(Vote,Post.id == Vote.post_id).where(Post.id == id).group_by(Post.id))).mappings().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    return post


@router.put("/update-post/{id}",response_model=schemas.PostResponseUser)
async def updatePostById(updated_post: schemas.PostCreate ,id: int , session: AsyncSession = Depends(get_async_session),user_id : schemas.TokenData = Depends(oauth2.get_current_user)):
    post = await session.scalar(select(Post).where(Post.id == id))
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    if post.user_id != int(user_id.id):
        raise HTTPException(status_code=403, detail=f"You are not allowed to delete this post")
    post.title = updated_post.title
    post.content = updated_post.content
    await session.commit()
    await session.refresh(post)
    return post

@router.delete("/delete-post/{id}",status_code=204)
async def deletePostById(id: int , sessions: AsyncSession = Depends(get_async_session),user_id : schemas.TokenData = Depends(oauth2.get_current_user)):
    post = await sessions.scalar(select(Post).where(Post.id == id))
    if not post:
        raise HTTPException(status_code=404, detail=f"No Post found with id : {id}")
    if post.user_id != int(user_id.id):
        raise HTTPException(status_code=403, detail=f"You are not allowed to delete this post")
    await sessions.delete(post)
    await sessions.commit()
    return {"deleted":True}

@router.get("/user-posts",response_model = List[schemas.PostResponseUser])
async def getUserPosts(session : AsyncSession = Depends(get_async_session),user_id : schemas.TokenData = Depends(oauth2.get_current_user)):
    posts = await session.scalars(select(Post).options(joinedload(Post.user)).where(Post.user_id == int(user_id.id)))
    return posts






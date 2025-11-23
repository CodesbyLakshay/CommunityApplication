from .. import models , schemas , utils , oauth2
from fastapi import Depends, HTTPException ,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_async_session
from ..models import User

router = APIRouter()
@router.post("/create-user",status_code=201,response_model=schemas.UserResponse)
async def create_user(user : schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = models.User(email=user.email, password=utils.hash(user.password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/get-user/{id}" , response_model=schemas.UserResponse)
async def get_user(id: int,session: AsyncSession = Depends(get_async_session),user_id : str = Depends(oauth2.get_current_user)):
    user = await session.scalar(select(User).where(User.id == id))
    if not user:
        raise HTTPException(status_code=404, detail=f"No User found with id : {id}")
    return user
from fastapi import APIRouter, Depends , HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_async_session
from .. import schemas,oauth2
from ..models import Vote

router = APIRouter()


@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(user_vote: schemas.Vote , session: AsyncSession = Depends(get_async_session) , user_id: str = Depends(oauth2.get_current_user)):

    vote = await session.scalar(select(Vote).filter(Vote.user_id == int(user_id.id)) , user_vote.post_id == Vote.post_id)
    if user_vote.vote_dir == 1:
        if vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f" user: {user_id.id} has already voted on post : {user_vote.post_id}")
        else:
            new_vote = Vote(post_id=user_vote.post_id, user_id=int(user_id.id))
            print(new_vote)
            session.add(new_vote)
            await session.commit()
        return {"message":"Vote Added"}
    else:
        if not vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Vote Found")
        else:
            await session.delete(vote)
            await session.commit()
        return {"message":"Vote Deleted"}

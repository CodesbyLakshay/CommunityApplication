from fastapi import APIRouter, Depends , HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_async_session
from .. import schemas , models , utils ,oauth2
from ..models import User

router = APIRouter()

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,session: AsyncSession = Depends(get_async_session)):
    user = await session.scalar(select(User).where(User.email == user_credentials.username))
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect credentials")
    if not  utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}
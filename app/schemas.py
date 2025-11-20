from typing import Optional,List
from pydantic import BaseModel, ConfigDict ,EmailStr,conint
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class UserResponse(BaseModel):
    id: int
    email:EmailStr
    created_At: datetime

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int

class UserVote(BaseModel):
    user_id: int
    post_id: int

class PostResponseUser(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int
    user: UserResponse
    vote: List[UserVote]

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    vote_dir:conint(le=1)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str



class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

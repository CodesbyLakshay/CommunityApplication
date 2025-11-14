import datetime

from .database import Base
from sqlalchemy import Integer, String, Boolean, DateTime, func, text
from sqlalchemy.orm import  Mapped, mapped_column

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content: Mapped[str] = mapped_column(String,nullable=False)
    published: Mapped[bool] = mapped_column(Boolean,default=True,server_default=text("true"))
    created_at: Mapped[datetime.timezone] = mapped_column(DateTime,nullable=False)

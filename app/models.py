import datetime
from typing import List
from .database import Base
from sqlalchemy import Integer, String, Boolean, DateTime, text, Nullable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content: Mapped[str] = mapped_column(String,nullable=False)
    published: Mapped[bool] = mapped_column(Boolean,default=True,server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False,)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,)
    user : Mapped["User"] = relationship("User")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email: Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False)
    created_At:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False,)

class Vote(Base):
    __tablename__ = "votes"

    post_id: Mapped[int] = mapped_column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True , nullable=False)
    user_id : Mapped[int] = mapped_column(Integer , ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)

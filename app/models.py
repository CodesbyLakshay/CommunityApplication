import datetime

from .database import Base
from sqlalchemy import Integer, String, Boolean, DateTime, text
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    content: Mapped[str] = mapped_column(String,nullable=False)
    published: Mapped[bool] = mapped_column(Boolean,default=True,server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False,)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email: Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False)
    created_At:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False,)
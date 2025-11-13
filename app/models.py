from database import Base
from sqlalchemy import column,Index,Integer,String, Text, DateTime,func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[Integer] = mapped_column(Integer,primary_key=True,index=True)
    title: Mapped[String] = mapped_column(String,nullable=False)
    content: Mapped[String] = mapped_column(String,nullable=False)
    published: Mapped[bool] = mapped_column(bool,default=True)

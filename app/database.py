from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


engine = create_async_engine(
    url='postgresql://postgres:fastapi@localhost/fastapi',
    echo=True
)

class Base(declarative_base):
    pass  

async def create_db():
    async with engine.begin() as conn:
        from models import Post
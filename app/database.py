from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData

engine = create_async_engine(
    url='postgresql+asyncpg://postgres:fastapi@localhost:5432/fastapi',
    echo=True
)

async_session_maker = async_sessionmaker(bind=engine,expire_on_commit=False)

class Base(DeclarativeBase):
    metadata = MetaData()

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session



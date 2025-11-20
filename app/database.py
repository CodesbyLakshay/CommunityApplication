from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData
from .config import settings

engine = create_async_engine(
    url=f'postgresql+asyncpg://{settings.db_name}:{settings.db_username}@{settings.db_hostname}:{settings.db_port}/{settings.db_password}',
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



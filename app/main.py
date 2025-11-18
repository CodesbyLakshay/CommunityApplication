from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import  create_db
from .routers import posts,users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(posts.router, prefix="/posts")
app.include_router(users.router, prefix="/users")


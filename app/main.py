from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import  create_db
from .routers import posts,users,auth,vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(posts.router, prefix="/posts",tags=["posts"])
app.include_router(users.router, prefix="/users",tags=["users"])
app.include_router(auth.router , prefix="/auth",tags=["auth"])

app.include_router(vote.router , prefix="/vote",tags=["vote"])

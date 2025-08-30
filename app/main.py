from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database , models 
from contextlib import asynccontextmanager
from .routers import users , posts , auth , votes
from sqlalchemy import text
    





 
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await database.engine.dispose()
app = FastAPI(lifespan=lifespan)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def main_root():
    return {"Hello FastAPI"}
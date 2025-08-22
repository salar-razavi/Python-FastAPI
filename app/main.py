from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database , models 
from contextlib import asynccontextmanager
from .routers import users , posts , auth

    


""" 
all_posts = [] """
""" app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 """
 
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await database.engine.dispose()
app = FastAPI(lifespan=lifespan)
 
 
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



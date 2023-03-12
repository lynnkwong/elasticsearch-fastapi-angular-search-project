from fastapi import FastAPI

from app.routers import posts

app = FastAPI()

app.include_router(posts.router, prefix="/posts")

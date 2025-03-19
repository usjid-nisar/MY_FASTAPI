from fastapi import FastAPI
from typing import Optional
from sqlalchemy.orm import Session
from .database import engine
from . import models
import sys
import os
from routers import post, users, auth, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

# Routes
@app.get("/")
def root():
    return {"message": "Hello world"}

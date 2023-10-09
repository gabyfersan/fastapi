from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "Favotite foods", "content": "I like pizza", "id": 2}]

try:
    # Connect to your postgres DB
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='Query1234', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Connection to database was succesfull')
except Exception as error:
    print('Connection to database failed')
    print('Error', error)


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI();

class Post(BaseModel): 
    title: str
    content: str
    published: bool=True

my_posts =[ {"title": "title of post 1", "content": "content of post 1", "id":1},
           {"title": "Favotite foods", "content": "I like pizza", "id":2}]

try:
# Connect to your postgres DB
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Query1234', cursor_factory=RealDictCursor) 
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
    for i , p in enumerate(my_posts):
        if p["id"] == id :
            return i

@app.get("/")
async def root():
    return {"message" : "Hello world"}

@app.get("/sqlal")
def test_post( db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return { 'data': posts }

@app.get("/posts")
def get_posts(db : Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"date": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute(""" INSERT INTO posts (title , content, published ) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    posts = cursor.fetchone()
    conn.commit()
    # post_dump = post.model_dump()
    # post_dump['id']= randrange(0,100000)
    # my_posts.append(post_dump)
    return {"date" : posts }


@app.get("/posts/{id}")
def get_post(id: int, reponse: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))  
    post = cursor.fetchone()
 
    print(post)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                             detail=f"post with id: {id} was not found")
    
    return {"post_detail": post }

 
@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = find_index_post(id)

    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    conn.commit()
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    cursor.execute(""" UPDATE  posts SET title= %s,  content= %s, published= %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    post_put= cursor.fetchone()
    conn.commit()
    #index = find_index_post(id)
    if post_put == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    return {"meaase": post_put}
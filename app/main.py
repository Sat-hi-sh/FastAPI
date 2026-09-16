from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = "localhost", database = "fastapi", user = "postgres", password = "Developer@24", cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database has been connected Successfully")
        break

    except Exception as error:
        print("Database Connectivity Failed")
        print("Error :", error)
        time.sleep(2)

my_post= [{"title" : "Post no 1" , "content" : "Content no 1", "id" : 1}, 
          {"title" : "Favourate Food", "Content" : "Briyani", "id" : 2}]

def find_post(id):
    for p in my_post:
        if p["id"] ==id:
            return p

        
def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "Hii Buddies"}

@app.get("/posts",response_model =List[schemas.Post])
def read_root(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # post = cursor.fetchall();
    posts = db.query(models.Post).all()
    return posts 


@app.post("/post", status_code = status.HTTP_201_CREATED, response_model =schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO  posts (title,content) VALUES (%s, %s) RETURNING * """,
    #               (post.title, post.content))
    #new_post =  cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, pulished = post.published)
    new_post = models.Post(**post.dict())
  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/{id}", response_model =schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM POSTs WHERE id = %s""", (str(id)))
    #one_post = cursor.fetchone()
    one_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not one_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not found")
    return one_post

@app.delete("/post/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM POSTs WHERE id = %s RETURNING * """, (str(id),))
    #delete_post = cursor.fetchone()
    #print(delete_post)
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f"post with id = {id} was not existed")

    post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)  


@app.put("/posts/{id}",response_model =schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id = {id} does not exist"
        )

    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return post_query.first()
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas,utils
from .database import engine, get_db
from .routers import post, user, auth

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Hii Buddies"}
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

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

@app.get("/post")
def read_root():
    cursor.execute("""SELECT * FROM post""")
    post = cursor.fetchall();
    return {"message": post}    

@app.post("/post", status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO  post (title,content) VALUES (%s, %s) RETURNING * """,
                   (post.title, post.content))
    new_post =  cursor.fetchone()
    conn.commit()
    return {"Detail": new_post}

@app.get("/post/{id}")
def get_one_post(id: int):
    cursor.execute("""SELECT * FROM POST WHERE id = %s""", (str(id)))
    one_post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not found")
    return {"Name": one_post}

@app.delete("/post/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("""DELETE FROM POST WHERE id = %s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    print(delete_post)
    conn.commit()
    if delete_post == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not existed")
    return Response(status_code = status.HTTP_204_NO_CONTENT)  


@app.put("/post/{id}")
def update_post(id :int, post : Post):
   
    cursor.execute("""UPDATE POST SET title = %s, content =%s WHERE id = %s RETURNING * """,
                    (post.title, post.content, str(id),))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not existed")

    return {"message" : update_post}
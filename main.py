from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_post= [{"title" : "Post no 1" , "content" : "Content no 1", "id" : 1}, 
          {"title" : "Favourate Food", "Content" : "Briyani", "id" : 2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

        
def find_post_index(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": my_post}

@app.post("/post", status_code = status.HTTP_201_CREATED)
def get_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_post.append(post_dict)
    return {"Name": my_post}

@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not found")
    return {"Name": post}

@app.delete("/post/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    index = find_post_index(id)
    if index == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not existed")
    my_post.pop(index)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
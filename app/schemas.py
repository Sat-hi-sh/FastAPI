from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass 

class Userout(BaseModel):
     id : int
     email : EmailStr
     timestamp : datetime

class Post(PostBase):
    id : int
    timestamp : datetime
    owner_id : int
    owner : Userout

class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: int | None = None
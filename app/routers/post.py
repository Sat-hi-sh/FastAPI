
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from requests import Session

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)

@router.get("/",response_model =List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM post""")
    # post = cursor.fetchall();
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model =schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO  posts (title,content) VALUES (%s, %s) RETURNING * """,
    #               (post.title, post.content))
    #new_post =  cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, pulished = post.published)

    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model =schemas.PostOut)
def get_one_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM POSTs WHERE id = %s""", (str(id)))
    #one_post = cursor.fetchone()
    # one_post = db.query(models.Post).filter(models.Post.id == id).first()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.id == id).first()
       
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id = {id} was not found")
    return posts

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM POSTs WHERE id = %s RETURNING * """, (str(id),))
    #delete_post = cursor.fetchone()
    #print(delete_post)
    #conn.commit()
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f"post with id = {id} was not existed")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= f"Unauthorized user to delete this post")

    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)  


@router.put("/{id}",response_model =schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    print(current_user.email)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id = {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail= f"Unauthorized user to update this post")

    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return post_query.first()
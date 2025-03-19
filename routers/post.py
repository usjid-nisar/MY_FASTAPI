from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from httpx import post

from sqlalchemy.orm import Session

from app.oauth2 import get_current_user

from app.database import get_db  
from app.database import engine  

from app import models, schemas, oauth2

from typing import List, Optional

from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


def test_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


# Route to get all posts
#@router.get("/", response_model=List[schemas.Post]) 
@router.get("/")# Fixed response model syntax
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
  #  posts = (
  #      db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()   
   # )
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isOuter=True).group_by(models.Post.id)
    filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    
    return posts


# Route to create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):


    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Route to get a single post by ID
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id).first()
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isOuter=True).group_by(models.Post.id)
    filter(models.Post.id == id).first()
    
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized"
        )
    return post


# Route to delete a post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
  
    
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Route to update a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

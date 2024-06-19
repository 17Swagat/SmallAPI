from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils, schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



@router.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # Using ORM:
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # Using ORM:
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id: {id} not found!!",
        )
    return post #{"post": post}


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    # Using ORM:
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
        )
    post.delete(synchronize_session=False)
    db.commit()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    
    # print('\n')
    # print(current_user.id)
    # print(current_user.email)
    # print(current_user.password)
    # print(current_user.created_at)
    # print('\n')

    # Using ORM:
    newpost = models.Post(creator_id=current_user.id,
                          **post.model_dump())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)  
    return newpost


@router.put("/update/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    # Using ORM:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with id: {id}",
        )
    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first() #{"post": post_query.first()}
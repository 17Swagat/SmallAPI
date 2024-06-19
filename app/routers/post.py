from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils, schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



@router.get("/allposts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # Using ORM:
    posts = db.query(models.Post).all()
    return posts


# @router.get("/{id}", response_model=schemas.Post)
# def get_post_by_postID(post_id: int, db: Session = Depends(get_db)):
#     # Using ORM:
#     post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if post is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with Id: {id} not found!!",
#         )
#     return post #{"post": post}


@router.get('/' , response_model=List[schemas.Post_CurrentUser])
def get_all_posts_by_currentUser(current_user: int = Depends(oauth2.get_current_user),
                                 db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.creator_id == current_user.id)
    posts = post_query.all()
    return posts

    # 2
    # Convert to Pydantic models and then to dictionaries
    # posts_dict = [schemas.Post_CurrentUser.model_validate(post).model_dump() for post in posts]
    # Example modification: add a new field
    # for post_dict in posts_dict:
    #     post_dict.pop('')
    # return posts_dict



@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    # Using ORM:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
        )

    if post.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Post:{id} doesn't belong to user:{current_user.id} "
        )


    post_query.delete(synchronize_session=False)
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
    
    if post.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Post:{id} doesn't belong to user:{current_user.id} "
        )

    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first() #{"post": post_query.first()}
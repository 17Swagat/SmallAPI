from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from typing import List

# from .schemas import Post
from . import schemas

# utils:
from . import utils

# PostgreSQL DB adapter
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLAlchemy:
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


# sqlAlchemy stuff:
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        connnection = psycopg2.connect(
            host="localhost",
            dbname="api_dev",
            user="postgres",
            password="helloPostgresql",
            cursor_factory=RealDictCursor,
        )  # to also get 'col-names' along with rows.
        cursor = connnection.cursor()
        print("\nDatabase connection successfull!!\n")
        break
    except Exception as error:
        print("\nDatabase connnection failed")
        print(f"Error: {error}\n")
        time.sleep(3)


@app.get("/")
def root():
    return {"message": "yo homie"}

@app.get("/posts", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db)):
    # Using ORM:
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # Using ORM:
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id: {id} not found!!",
        )
    return post #{"post": post}


@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # Using ORM:
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
        )
    post.delete(synchronize_session=False)
    db.commit()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Using ORM:
    newpost = models.Post(**post.model_dump())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)  # retrieving the newly created post
    return newpost #{"post": newpost}


@app.put("/posts/update/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
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


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session=Depends(get_db)):

    # hashing the pswd:
    # hashed_pswd = pwd_context.hash(secret=user.password)
    # user.password = hashed_pswd
    user.password = utils.hash_pswd(user.password)
    
    # saving to DB:
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
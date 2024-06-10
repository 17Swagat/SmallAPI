from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from typing import List

# from .schemas import Post
from . import schemas

# PostgreSQL DB adapter
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLAlchemy:
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

# * create the database tables based on the SQLAlchemy models defined in your models module.
# * Does not alter existing tables or delete existing data. It only creates tables that do not already exist in the database. If a table already exists, create_all will skip creating that table and leave the existing table and its data unchanged.
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
    # cursor.execute(query="""SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(query="""SELECT * from posts where post_id = %s""", vars=(id,))
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with Id: {id} not found!!",
    #     )
    # return {"post": post}

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
    # cursor.execute(query=""" select * from posts where id = %s""", vars=(id,))
    # post = cursor.fetchone()
    # # if post not available:
    # if post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
    #     )
    # # if post available:
    # cursor.execute(query=""" delete from posts where id = %s returning *""", vars=(id,))
    # deleted_post = cursor.fetchone()

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
    # cursor.execute(
    #     query="""insert into posts(title, content, published) values (%s, %s, %s) returning *""",
    #     vars=(post.title, post.content, post.published),
    # )
    # newpost = cursor.fetchone()
    # connnection.commit()
    # return {"post": newpost}

    # Using ORM:
    newpost = models.Post(**post.model_dump())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)  # retrieving the newly created post
    return newpost #{"post": newpost}


@app.put("/posts/update/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     # update posts set title = title, content = content where id = id
    #     query=""" update posts set title = %s, content = %s, published = %s where id = %s returning *""",
    #     vars=(updated_post.title, updated_post.content, updated_post.published, id),
    # )
    # post = cursor.fetchone()
    # if post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post not found with id: {id}",
    #     )
    # connnection.commit()
    # return {"updated_post": post}

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

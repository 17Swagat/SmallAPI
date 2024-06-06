from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange

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


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    # rating: Optional[int] = 15


@app.get("/")
def root():
    return {"message": "yo homie"}


# Testing ORM:
@app.get("/testing/")
def test_posts(db: Session = Depends(get_db)):
    # performing SQL queries via ORM
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute(query="""SELECT * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
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
    return {"post": newpost}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(query="""SELECT * from posts where post_id = %s""", vars=(id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id: {id} not found!!",
        )
    return {"post": post}


@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(query=""" select * from posts where id = %s""", vars=(id,))
    post = cursor.fetchone()
    # if post not available:
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
        )
    # if post available:
    cursor.execute(query=""" delete from posts where id = %s returning *""", vars=(id,))
    deleted_post = cursor.fetchone()


@app.put("/posts/update/{id}")
def update_post(id: int, updated_post: Post):
    cursor.execute(
        # update posts set title = title, content = content where id = id
        query=""" update posts set title = %s, content = %s, published = %s where id = %s returning *""",
        vars=(updated_post.title, updated_post.content, updated_post.published, id),
    )
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with id: {id}",
        )
    connnection.commit()
    return {"updated_post": post}

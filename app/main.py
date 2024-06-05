from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# PostgreSQL DB adapter
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = 15


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

my_posts = [
    {"title": "title post 1", "content": "content post 1", "id": 1},
    {"title": "favourite food", "content": "i like pizza", "id": 2},
]


@app.get("/")
def root():
    return {"message": "yo homie"}


@app.get("/posts")
def get_post():
    cursor.execute(query="""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        query="""SELECT * from posts where id = %s""", vars=(id,)
    )  # @instructor: `vars = str(id)`
    post = cursor.fetchone()
    if post is None:  # post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id: {id} not found!!",
        )
    return {"post": post}


@app.delete("/posts/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(query=""" delete from posts where id = %s returning *""", vars=(id,))
    deleted_post = cursor.fetchone()
    if delete_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found= id:{id}"
        )
    connnection.commit()
    return {"deleted post": delete_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        query="""insert into posts(title, content, published) values (%s, %s, %s) returning *""",
        vars=(post.title, post.content, post.published),
    )
    newpost = cursor.fetchone()
    connnection.commit()
    return {"post": newpost}


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

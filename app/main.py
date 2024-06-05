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
        connnection = psycopg2.connect(host='localhost', 
                                    dbname='api_dev', 
                                    user='postgres',
                                    password='helloPostgresql',
                                    cursor_factory=RealDictCursor) # to also get 'col-names' along with rows.
        cursor = connnection.cursor()
        print('\nDatabase connection successfull!!\n')
        break
    except Exception as error:
        print('\nDatabase connnection failed')
        print(f'Error: {error}\n')
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
    cursor.execute(query='''SELECT * from posts''')
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # ❌ AVOID: hardcoding:
    # cursor.execute(
    #     # query=f'''insert into posts(title, content, published) values ({post.title, post.content, post.published})''')
    
    # ✅ BETTER & SAFER way: 
    # This method uses parameterized queries
    cursor.execute(
        query='''insert into posts(title, content, published) values (%s, %s, %s) returning *''',
        vars=(post.title, post.content, post.published)
    )
    newpost = cursor.fetchone()
    connnection.commit()
    return {"post":newpost}


@app.get("/posts/{id}")
def get_post(id: int):
    """Getting a specific post"""
    for post in my_posts:
        # post-found:
        if post["id"] == id:
            return {"post": post}
    # post-not-found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'post not found with id:{id}')




@app.delete('/posts/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    for index, post in enumerate(my_posts):
        # id-matched!!
        if post['id'] == id:
            my_posts.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    # Can't Find Element To Delete
    # of given: id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post not found= id:{id}')


@app.put('/posts/update/{id}')
def update_post(id: int, updated_post: Post):
    
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            my_posts[index]['title'] = updated_post.title
            my_posts[index]['content'] = updated_post.content
            my_posts[index]['published'] = updated_post.published
            my_posts[index]['rating'] = updated_post.rating
            return {'message': 'Post updated successfully', 'post': my_posts[index]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post not found with id: {id}')

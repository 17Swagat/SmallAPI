from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
# PostgreSQL DB adapter
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = 15

# CONNECTING TO A DATABASE:
try:
    # Connect to an existing database
    connnection = psycopg2.connect(host='localhost', 
                                   dbname='api_dev', 
                                   user='postgres',
                                   password='helloPostgresql',
                                   cursor_factory=RealDictCursor) # to also get 'col-names' along with rows.
    # Open a cursor to perform database operations
    cursor = connnection.cursor()
    print('\nDatabase connection successfull!!\n')

except Exception as error:
    print('\nDatabase connnection failed')
    print(f'Error: {error}\n')

my_posts = [
    {"title": "title post 1", "content": "content post 1", "id": 1},
    {"title": "favourite food", "content": "i like pizza", "id": 2},
]


@app.get("/")
def root():
    return {"message": "yo homie"}


@app.get("/posts")
def get_post():
    return {"data": my_posts}



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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # saving into array
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # returning response
    return {"post": post_dict}


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

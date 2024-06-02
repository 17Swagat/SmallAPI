from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = False
    rating: Optional[int] = None

@app.get('/')
def root():
    return {'message': 'yo homie'}

@app.get('/login')
def get_user():
    return {'message': 'Hello world'}

@app.get('/posts')
def get_post():
    return {'data': 'this is your post'}

@app.post('/posts/create')
def create_posts(post:Post):
    return {'titlex': post.title, 'contentx': post.content, 'publishedx': post.published,\
            'rating':post.rating}

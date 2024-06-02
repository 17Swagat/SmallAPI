from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = False
    rating: Optional[int] = 15

my_posts = [{'title': 'title post 1', 'content': 'content post 1', 'id': 1}, {'title': 'favourite food', 'content': 'i like pizza', 'id': 2}]

@app.get('/')
def root():
    return {'message': 'yo homie'}

@app.get('/posts')
def get_post():
    return {'data': my_posts}

@app.get('/posts/{id}')
def get_post(id):
    '''Getting a specific post'''
    return {'type(id)': str(type(id))}
    for post in my_posts:
        if post['id'] == id:
            return {'post': post}
    return {'message': 'post not found'}


@app.post('/posts')
def create_posts(post: Post):
    # saving into array
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {'post': post_dict}

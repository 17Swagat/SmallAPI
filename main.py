from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get('/')
def root():
    return {'message': 'yo homie'}

@app.get('/login')
def get_user():
    return {'message': 'Hello world'}

@app.get('/posts')
def get_post():
    return {'data': 'this is your post'}

# @app.post('/createposts')
# def create_posts(payload: dict = Body(...)):
#     return {'post': payload, 'title': payload['title'], 'content': payload['content']}

@app.post('/posts/create')
def create_posts(post:Post):
    return {'titlex': post.title, 'contentx': post.content}

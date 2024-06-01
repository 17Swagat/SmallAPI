from fastapi import FastAPI

app = FastAPI()

# first "path" match gets selected
# Hence ordering is important

@app.get('/')
def root():
    return {'message': 'yo homie'}

@app.get('/login')
def get_user():
    return {'message': 'Hello world'}

@app.get('/posts')
def get_post():
    return {'data': 'this is your post'}
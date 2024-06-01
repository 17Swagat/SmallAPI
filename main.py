from fastapi import FastAPI

app = FastAPI()

@app.get('/login')
def get_user():
    return {'message': 'Hello world'}
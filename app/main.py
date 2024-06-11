from fastapi import Body, FastAPI #,Response, status, HTTPException, Depends

# from .schemas import Post
from . import schemas

# utils:
from . import utils

# PostgreSQL DB adapter
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLAlchemy:
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user

# sqlAlchemy stuff:
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB stuff(psycopg2):
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

# routes import:
app.include_router(router=post.router)
app.include_router(router=user.router)

@app.get("/")
def root():
    return {"message": "yo homie"}

# DEBUG:
import uvicorn

# FastAPI:
from fastapi import FastAPI 

# PostgreSQL DB adapter
# import psycopg2
# from psycopg2.extras import RealDictCursor

# SQLAlchemy:
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)

# routes:
from .routers import post, user, auth


app = FastAPI()

# DB stuff(psycopg2):
# while True:
#     try:
#         connnection = psycopg2.connect(
#             host="localhost",
#             dbname="api_dev",
#             user="postgres",
#             password="helloPostgresql",
#             cursor_factory=RealDictCursor,
#         )  # to also get 'col-names' along with rows.
#         cursor = connnection.cursor()
#         print("\nDatabase connection successfull!!\n")
#         break
#     except Exception as error:
#         print("\nDatabase connnection failed")
#         print(f"Error: {error}\n")
#         time.sleep(3)

# routes import:
app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)

@app.get("/")
def root():
    return {"message": "yo homie"}


# For debugging with breakpoints in VS-Code
if __name__ == '__main__':

    uvicorn.run(app=app, host='0.0.0.0', port=8000)
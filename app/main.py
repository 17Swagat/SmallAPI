# DEBUG:
import uvicorn

from fastapi import FastAPI


# SQLAlchemy:
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

# routes:
from .routers import post, user, auth, vote


app = FastAPI()


# routes import:
app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=vote.router)


@app.get("/")
def root():
    return {"message": "yo homie"}


# For debugging with breakpoints in VS-Code
if __name__ == "__main__":

    uvicorn.run(app=app, host="0.0.0.0", port=8000)

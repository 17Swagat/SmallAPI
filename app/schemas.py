from pydantic import BaseModel, EmailStr
from datetime import datetime
# from typing import Optional


# POST:
##################################
# Request(s):=>
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    # rating: Optional[int] = 15


class PostCreate(PostBase):
    pass


# Response:=>
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        # orm_mode = True # depreceated:
        from_attributes = True


# USER:
##################################
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response:=>
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        # orm_mode = True # depreacted:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
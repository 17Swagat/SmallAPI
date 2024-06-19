from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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


# Response:=> PostOut
class Post(PostBase):
    id: int
    created_at: datetime
    creator_id: int 
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    # id: Optional[int] = None
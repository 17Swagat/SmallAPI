from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


##################################
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

##################################
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
    '''use it: in case when all posts by all the users are in one place'''
    id: int
    created_at: datetime
    creator_id: int 
    owner: UserOut
    class Config:
        # orm_mode = True # depreceated:
        from_attributes = True


class Post_CurrentUser(PostBase):
    '''use it: when we need all the posts by current_user'''
    id: int
    created_at: datetime
    creator_id: int # not necessary to include it TBH [coz: Its for the current user]
    class Config:
        # orm_mode = True # depreceated:
        from_attributes = True
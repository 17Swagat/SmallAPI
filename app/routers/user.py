from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import utils, schemas, models
from ..database import get_db

router = APIRouter(
    prefix= '/user',
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db:Session=Depends(get_db)):
    # hashing the pswd:
    user.password = utils.hash_str(user.password)
    
    # saving to DB:
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id: {id} not found!!")
    return user


@router.get('/', response_model=List[schemas.UserOut])
def get_all_users(db:Session=Depends(get_db)):
    ''' Its better to not use this function, if no. of users are to many. [Or] 
     [@LATER]: Could set a limit: To how many users will be prompted each no. 
      of times. '''
    users = db.query(models.User).all()
    return users
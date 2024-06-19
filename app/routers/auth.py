from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from .. import utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), 
          # user_creds: schemas.UserLogin,
          db:Session = Depends(get_db)):
    
    # user = db.query(models.User).filter(models.User.email == user_creds.email).first()
    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No such user present. Create Account.')
    
    userverified = utils.verify_pswd(plain_pswd = user_creds.password, # user-provided-pswd
                                     hashed_pswd = user.password)      # DB stored -user-pswd
    if userverified == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong Password')
    
    # Create a token
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta, timezone
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# SECRET_KEY
SECRET_KEY = "e8e995839008cf1b5ef7f17fd15912a3b249f163ff25ba9dd4be4c0cd04d89b5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# ACCESS_TOKEN_EXPIRE_SECONDS = 30  


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    except PyJWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # token: TokenData(id='8')
    # token.id: '8'
    # type(token.id): str
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

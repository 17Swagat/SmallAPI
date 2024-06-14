import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
from datetime import timedelta

# SECRET_KEY
SECRET_KEY = 'e8e995839008cf1b5ef7f17fd15912a3b249f163ff25ba9dd4be4c0cd04d89b5'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(payload=to_encode, 
                             key=SECRET_KEY, 
                             algorithm=ALGORITHM)
    return encoded_jwt
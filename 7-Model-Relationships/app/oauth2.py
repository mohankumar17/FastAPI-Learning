from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = config.TOKEN_SECRET_KEY
ALGORITHM = config.TOKEN_ALGORITHM
EXPIRE_TIME_SECONDS = config.TOKEN_EXPIRE_TIME_SECONDS

def create_access_token(data: dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(seconds=EXPIRE_TIME_SECONDS)
    to_encode.update({"exp": expire_time})

    jwt_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def validate_access_token(access_token: str, UserCredsException):
    try:
        payload = jwt.decode(token=access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise UserCredsException
        
        token_data = schemas.TokenData(id = user_id)
        return token_data
    
    except JWTError:
        raise UserCredsException

def get_current_user(token: str = Depends(oauth2_scheme)):
    UserCredsException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Falied to validated the credentails", headers={"WWW-Authenticate": "Bearer"})

    return validate_access_token(token, UserCredsException)


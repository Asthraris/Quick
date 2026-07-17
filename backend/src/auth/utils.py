from datetime import datetime,timedelta,timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict , expires_delta: Optional[timedelta]=None) -> str:
    #mostly data is user name or id Which is verified before this so to gen token
    to_encode = data.copy()
    #set expiry time of the token
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION)

    # "exp" (Expiration Time): When the token dies (which you set right above in your code).
    # STANDARD DEFINED MY OAUTH2
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    
    return encoded_jwt



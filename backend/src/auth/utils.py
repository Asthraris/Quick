import bcrypt
from datetime import datetime,timedelta,timezone
from typing import Optional
from jose import jwt

from src.core.config import settings


def hash_password(password: str) -> str:
    # bcrypt requires bytes, so encode the plain text password string first
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the stored bcrypt hash string."""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Checkpw safely validates the password match
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False

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



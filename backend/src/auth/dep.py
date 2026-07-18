#FastAPI uses OAuth2PasswordBearer to automatically extract the token from the HTTP Authorization: Bearer <token> header.
from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError , jwt

from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.config import settings
from src.auth.model import User


#this is used to specify dat present in authorization header , here exact login path is saved 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#this mostly verifies that token at every request that this is the same user
#ALWAYS needs auth details and db session to work and returns user to server
def get_current_user(token: str = Depends(oauth2_scheme) , db :Session = Depends(get_db))-> User:
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        #decode the provided token
        payload = jwt.decode(token , settings.JWT_SECRET_KEY , algorithms=[settings.JWT_ALGORITHM])

        #DB LOGIC WORK UPON YR CODE
        user_id : str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Query your SQLAlchemy DB model to ensure the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
        
    return user

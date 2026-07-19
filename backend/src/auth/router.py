from fastapi import APIRouter , Depends , status , HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db 
from src.auth import service,schema
from src.core.exceptions import UserAlreadyExistsException,UserEmailNotExists,UserPasswordNotMatched


router = APIRouter(tags=["Authentication"] , prefix="/user")

@router.post("/login", response_model = schema.TokenSchema , status_code= status.HTTP_200_OK)
async def logIn(req :schema.UserInfo , db :Session = Depends(get_db)):
    try:
        return await service.authenticateUser(req=req,db=db)
    except UserEmailNotExists as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except UserPasswordNotMatched as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= str(err)
        )
    

@router.post("/register", response_model = schema.UserResponse , status_code= status.HTTP_201_CREATED )
async def Register(req :schema.UserInfo , db :Session = Depends(get_db) ):
    try:
        return await service.createUser(db=db, req=req)

    
    except UserAlreadyExistsException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

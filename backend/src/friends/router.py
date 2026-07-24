from fastapi import APIRouter,status , Depends , HTTPException
from src.auth.schema import UserResponse
from src.core.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from src.auth.model import User 
#ab sab jwt verification me ye use hoga
from src.auth.dep import get_current_user
from src.friends import service,schema
from typing import List
from src.core.exceptions import (
    SelfConnectionException,
    friendshipAlreadyExistsException,
    UserNotFound,
    friendshipRequestNotExists
)

router = APIRouter(tags=["User"] )

@router.get("/users/search" , response_model= UserResponse , status_code= status.HTTP_200_OK)
async def searchUser(
    usern :str ,
    db:Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)
    ):
    user_s = db.query(User).filter(User.username == usern).first()

    if not user_s:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= str(UserNotFound("Invalid Username"))
        )
    

    #i dont want to return the usermodel cause it contains passowrd feild even if its hashed
    user_res = UserResponse(
        id = user_s.id,
        is_active= user_s.is_active,
        username= user_s.username,
        email= user_s.email
    )
    return user_res


@router.post("/friends/{req_uuid}/send_req", response_model= schema.friendResponse , status_code= status.HTTP_200_OK )
async def send_request(
    req_uuid:UUID ,
    db:Session = Depends(get_db),
    curr_user : User = Depends(get_current_user) ):
    try:
        return await service.send_friendship_req(
            sender_id=curr_user.id,
            receiver_id=req_uuid,
            db=db
        )
    except SelfConnectionException as err:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= str(err)
        )
    except friendshipAlreadyExistsException as err:
        raise HTTPException(
            status_code= status.HTTP_429_TOO_MANY_REQUESTS,
            detail= str(err)
        )

#abhi me sent request ka baad me karunga , here only the list of incomming wale hi rakhta hu , since i not taking back rn
@router.get("/friends/requests/pending" , response_model=List[schema.friendResponse] , status_code=status.HTTP_200_OK)
async def checkRequests(
    curr_user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    return await service.fetch_all_req(
        reviecer_id= curr_user.id,
        db=db
    )

@router.patch("/friends/requests/{request_id}/accept" , response_model=schema.friendResponse , status_code=status.HTTP_200_OK)
async def acceptRequest(
    request_id : UUID,
    curr_user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    try:
        return await service.accept_req(
            sender_id = request_id,
            receiver_id= curr_user.id,
            db = db
        )
    except friendshipRequestNotExists as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(err))
    
@router.patch("/friends/requests/{request_id}/decline" , response_model=schema.friendResponse , status_code=status.HTTP_200_OK)
async def declineRequest(
    request_id : UUID,
    curr_user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    try:
        return await service.decline_req(
            sender_id = request_id,
            receiver_id= curr_user.id,
            db = db
        )
    except friendshipRequestNotExists as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(err))

@router.patch("/friends/requests/{request_id}/block" , response_model=schema.friendResponse , status_code=status.HTTP_200_OK)
async def blockRequest(
    request_id : UUID,
    curr_user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    try:
        return await service.block_req(
            sender_id = request_id,
            receiver_id= curr_user.id,
            db = db
        )
    except friendshipRequestNotExists as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(err))


    

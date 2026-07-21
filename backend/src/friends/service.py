from uuid import UUID
from sqlalchemy.orm import Session
from src.friends import model
from src.core.exceptions import (
    SelfConnectionException,
    friendshipAlreadyExistsException,
    friendshipRequestNotExists
)
from src.friends.schema import (
    friendResponse,
    friendStatus
    )

from typing import List

async def send_friendship_req(sender_id : UUID , receiver_id : UUID , db :Session):
    if sender_id == receiver_id:
        raise SelfConnectionException("You cannot send a connection request to yourself.")
    
    existing_ship = db.query(model.Friends).filter(
        model.Friends.sender_id == sender_id,
        model.Friends.receiver_id == receiver_id
    ).first()
    # abhi tak block and decline dono time same hi exception hoga and we cant send another req
    if existing_ship:
        raise friendshipAlreadyExistsException("A connection request already exists.")
    
    new_friendship = model.Friends(
        sender_id = sender_id,
        receiver_id = receiver_id,
        status = model.friendStatus.PENDING
    )

    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)

    res = friendResponse(
        sender_id= sender_id,
        receiver_id= receiver_id,
        status=friendStatus.PENDING
    )

    return res

async def fetch_all_req(reviecer_id :UUID , db:Session )->List[friendResponse]:
    return db.query(model.Friends).filter(
        model.Friends.receiver_id == reviecer_id ,
        model.Friends.status == friendStatus.PENDING )
    
async def accept_req(sender_id : UUID , receiver_id :UUID , db :Session) -> friendResponse:
    request = db.query(model.Friends).filter(
        model.Friends.sender_id == sender_id,
        model.Friends.receiver_id == receiver_id
    ).first()
    
    if not request:
        raise friendshipRequestNotExists("Friend request not found.")
    
    request.status = friendStatus.ACCEPTED
    db.commit()
    db.refresh(request)
    return request


    
async def decline_req(sender_id : UUID , receiver_id :UUID , db :Session):
    request = db.query(model.Friends).filter(
        model.Friends.sender_id == sender_id,
        model.Friends.receiver_id == receiver_id
    ).first()
    
    if not request:
        raise friendshipRequestNotExists("Friend request not found.")
    
    request.status = friendStatus.DECLINED
    db.commit()
    db.refresh(request)
    return request

async def block_req(sender_id : UUID , receiver_id :UUID , db :Session):
    request = db.query(model.Friends).filter(
        model.Friends.sender_id == sender_id,
        model.Friends.receiver_id == receiver_id
    ).first()
    
    if not request:
        raise friendshipRequestNotExists("Friend request not found.")
    
    request.status = friendStatus.BLOCKED
    db.commit()
    db.refresh(request)
    return request



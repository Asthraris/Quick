from pydantic import BaseModel
from uuid import UUID
from enum import Enum

#WAY TO DEFINE ENUMS IN PYTHON
class friendStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    BLOCKED = "blocked"

class friendResponse(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    status: friendStatus

    class Config:
        from_attributes = True
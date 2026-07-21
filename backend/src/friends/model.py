import enum
from sqlalchemy import Column  , ForeignKey , Enum , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base


#creating status enums for using in db
class friendStatus(str , enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    BLOCKED = "blocked"

class Friends(Base):
    __tablename__ = "friends"

    sender_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        primary_key=True
    )
    receiver_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id",ondelete="CASCADE"),
        primary_key=True
    )

    # CAN 2 column be primary in single table & what does Cascade mean like if user gets deleted 
    status = Column(Enum(friendStatus) , default=friendStatus.PENDING , nullable= False)

    # Prevents duplicate active requests between the same two people
    # Note: Removed redundant UniqueConstraint since primary_key=True on both columns enforces uniqueness!
    

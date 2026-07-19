import enum
from sqlalchemy import Column , String , ForeignKey , Enum , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from core.database import Base


#creating status enums for using in db
class friendStatus(str , enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class Friends(Base):
    __tablename__ = "friends"

    sender_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id",ondelete="CASCADE"),
        primary_key=True
    )
    sender_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id",ondelete="CASCADE"),
        primary_key=True
    )

    # CAN 2 column be primary in single table & what does Cascade mean like if user gets deleted 
    status = Column(Enum(friendStatus) , default=friendStatus.DECLINED , nullable= False)

    # Prevents duplicate active requests between the same two people
    __table_args__ = (
        UniqueConstraint('sender_id', 'receiver_id', name='uq_sender_receiver'),
    )

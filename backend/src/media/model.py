from sqlalchemy import Column,String,DateTime,ForeignKey,Integer,text
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base
import uuid


class Media(Base):
    __tablename__ = "medias"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        #genarate using uuid package but stored in postgreporvided UUID
        default=uuid.uuid4
    )
    url = Column(String,nullable=False)

    # Storage bucket key (needed to locate and delete the file from S3 later)
    file_key = Column(String, nullable=False, unique=True)

    uploader_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Metadata
    file_type = Column(String, nullable=False)  # e.g., 'image/png'
    file_size_bytes = Column(Integer, nullable=True)  # e.g., 204800 (200 KB)

    posted_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    #IMP for worker thread to know which media is expired so it can deleate them as thread.time.now > expiries_at
    #ALSO we can always see if the user can access this resources in 24 hrs deadline
    expiries_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP + INTERVAL '24 hours'"),
        nullable=False
    )


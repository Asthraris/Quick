from sqlalchemy import Column,ForeignKey , DateTime , text
from sqlalchemy.dialects.postgresql import UUID

from src.core.database import Base

class MediaAudit(Base):
    __tablename__ = "media_audit"

    media_id = Column(
        UUID(as_uuid= True),
        ForeignKey("medias.id" , ondelete="CASCADE"),
        primary_key=True
    )

    viewer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id" , ondelete="CASCADE"),
        primary_key= True
    )

    viewed_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
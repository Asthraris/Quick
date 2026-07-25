from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.media import model as media_model
from src.viewone import model as audit_model
from src.core.exceptions import (
    ImageNotFoundException,
    ImageExpiredException,
    ImageAlreadyViewedException,
    MediaDatabaseException,
)


async def consume_and_log_image_view(
    im_id: UUID, 
    viewer_id: UUID, 
    db: Session
) -> str:
    now = datetime.now(timezone.utc)

    # 1. Fetch image record safely
    try:
        media_res = db.query(media_model.Media).filter(
            media_model.Media.id == im_id,
            media_model.Media.status == "ACTIVE",
        ).first()
    except SQLAlchemyError as err:
        raise MediaDatabaseException("Failed to query image from database.") from err

    # Check 1: Existence
    if not media_res:
        raise ImageNotFoundException(f"Image with ID '{im_id}' was not found.")

    # Check 2: Expiration (> 24 hours)
    if media_res.expiries_at <= now:
        raise ImageExpiredException("This image has passed its 24-hour expiration window.")

    # Check 3: Self-view restriction (optional: prevents uploader from consuming their own story)
    # if image.uploader_id == viewer_id:
    #     raise ImageUnauthorizedAccessException("Uploaders cannot consume their own view-once media.")

    # 2. Check if already viewed by this user
    try:
        already_viewed = db.query(audit_model.MediaAudit).filter(
            audit_model.MediaAudit.image_id == im_id,
            audit_model.MediaAudit.viewer_id == viewer_id
        ).first()
    except SQLAlchemyError as err:
        raise MediaDatabaseException("Failed to check audit table status.") from err

    if already_viewed:
        raise ImageAlreadyViewedException("You have already consumed this image.")

    # 3. Write audit log with transaction safety (rollback on fail)
    try:
        new_audit_rec = audit_model.MediaAudit(
            image_id=im_id,
            viewer_id=viewer_id
        )
        db.add(new_audit_rec)
        db.commit()
    except IntegrityError:
        db.rollback()
        # Handles race conditions where two simultaneous requests try to view the image at once
        raise ImageAlreadyViewedException("Concurrent request detected. Image already viewed.")
    except SQLAlchemyError as err:
        db.rollback()
        raise MediaDatabaseException("Failed to record view audit log in database.") from err

    return media_res.url
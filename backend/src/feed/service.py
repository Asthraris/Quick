from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from src.auth.model import User
from src.friends.service import GetAllFriends
from src.media import model as media_model
from src.viewone.model import MediaAudit
from src.core.exceptions import (
    MediaDatabaseException,
    NoFriendsFoundException,
    EmptyFeedException,
)


async def fetchEntireFeed(db: Session, curr_user: User) -> List[media_model.Media]:
    user_id = curr_user.id
    now = datetime.now(timezone.utc)

    # 1. Fetch friend subquery safely
    try:
        friends =await GetAllFriends(db, user_id=user_id)
    except SQLAlchemyError as err:
        raise MediaDatabaseException("Failed to retrieve user's friends list.") from err

    if friends is None:
        raise NoFriendsFoundException("User has no active friend connections.")

    # 2. Execute single-pass join query safely
    try:
        feed_images = (
            db.query(media_model.Media)
            .outerjoin(
                MediaAudit,
                and_(
                    media_model.Media.id == MediaAudit.media_id,
                    MediaAudit.viewer_id == user_id,
                ),
            )
            .filter(
                media_model.Media.uploader_id.in_(friends),
                media_model.Media.status == "ACTIVE",
                media_model.Media.expiries_at > now,      # Exclude expired
                MediaAudit.media_id == None,  # Exclude already viewed
            )
            .order_by(media_model.Media.posted_at.desc())
            .all()
        )
    except SQLAlchemyError as err:
        raise MediaDatabaseException("Failed to query unviewed feed images from database.") from err

    # 3. Handle empty state optional check
    # Note: If returning an empty list [] is preferred for the frontend, you can remove this check.
    if not feed_images:
        raise EmptyFeedException("No active unviewed stories found from your friends.")

    return feed_images
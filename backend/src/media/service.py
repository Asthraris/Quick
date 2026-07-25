import uuid
from uuid import UUID
from src.core.s3 import generate_presigned_post_url , get_s3_object_metadata
from src.core.exceptions import (
    MediaDatabaseException,

    ImageNotFoundException,
    CorruptedUploadException,
    MediaDatabaseException,

)
from src.media.schema import PresignedUploadResponse ,mediaMetaData
from sqlalchemy.orm import Session
from src.media.utils import validate_upload_request,MAX_FILE_SIZE_BYTES
from src.media import model
from sqlalchemy.exc import SQLAlchemyError





async def uploadRequest(metadata : mediaMetaData , uploaders_id , db :Session)->PresignedUploadResponse:
    # 1. Validate requested metadata (type and size)
    validate_upload_request(
        file_type=metadata.file_type, 
        file_size_bytes=metadata.file_size_bytes
    )
    # 2. Generate a unique S3 storage key
    # e.g., "pending/8c3df12d-94a2-4a41-b841-332e1284fa0a/a1b2c3d4-..."
    unique_media_id = uuid.uuid4()
    file_extension = metadata.file_type.split("/")[-1]
    file_key = f"pending/{uploaders_id}/{unique_media_id}.{file_extension}"

    # 3. Save pending upload log to PostgreSQL
    try:
        new_media_rec = model.Media(
            id=unique_media_id,
            file_key=file_key,
            uploader_id=uploaders_id,
            file_type=metadata.file_type,
            file_size_bytes=metadata.file_size_bytes,
            status="PENDING"
        )
        db.add(new_media_rec)
        db.commit()
        db.refresh(new_media_rec)
    except SQLAlchemyError as err:
        db.rollback()
        raise MediaDatabaseException("Failed to register pending upload in database.") from err

    # 4. Generate S3 presigned POST dictionary
    s3_post_data = generate_presigned_post_url(file_key=file_key, file_type=metadata.file_type)

    # 5. Return schema containing upload target info + media_id for confirmation
    return PresignedUploadResponse(
        media_id=new_media_rec.id,
        file_key=file_key,
        upload_url=s3_post_data["url"],
        fields=s3_post_data["fields"]
    )




#USED WHEN FRONTEND IS DONE UPLOADING FILE THEN ACKNOWLEDGES THE BACKEND
async def confirm_media_upload(
    media_id: UUID, 
    uploader_id: UUID, 
    db: Session
) -> model.Media:
    
    # 1. Fetch pending record from database
    try:
        media_rec = db.query(model.Media).filter(
            model.Media.id == media_id,
            model.Media.uploader_id == uploader_id,
            model.Media.status == "PENDING"
        ).first()
    except SQLAlchemyError as err:
        raise MediaDatabaseException("Failed to query upload log from database.") from err

    if not media_rec:
        raise ImageNotFoundException("No pending upload found matching this ID.")

    # 2. Inspect real object directly in S3
    s3_meta = get_s3_object_metadata(file_key=media_rec.file_key)

    actual_size = s3_meta["size_bytes"]
    actual_mime = s3_meta["mime_type"]

    # 3. Verify actual S3 metadata against safety constraints //yaha par mene mime comparison add kiya hai usme kuch error/bug aa sakta hai
    if actual_size > MAX_FILE_SIZE_BYTES or actual_size == 0 or media_rec.file_size_bytes != actual_size or media_rec.file_type != actual_mime:
        # Clean up database record if invalid
        try:
            db.delete(media_rec)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
        raise CorruptedUploadException("Uploaded file size violates policy bounds.")

    # 4. Activate record for feed availability
    try:
        media_rec.status = "ACTIVE"
        media_rec.file_size_bytes = actual_size  # Store actual uploaded size
        db.commit()
        db.refresh(media_rec)
    except SQLAlchemyError as err:
        db.rollback()
        raise MediaDatabaseException("Failed to activate media record in database.") from err

    return media_rec

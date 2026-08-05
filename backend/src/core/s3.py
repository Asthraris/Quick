import boto3
from botocore.exceptions import BotoCoreError, ClientError
from src.core.config import settings
from src.media.utils import MAX_FILE_SIZE_BYTES
from src.core.exceptions import MediaDatabaseException, UploadConfirmationFailedException

# Check if we are running in local demo mode
IS_LOCAL_DEMO = (
    getattr(settings, "AWS_ACCESS_KEY_ID", "").lower() == "local" or 
    getattr(settings, "S3_BUCKET_NAME", "").lower() == "local"
)

# Initialize client only if not in local demo mode
s3_client = None if IS_LOCAL_DEMO else boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)


def generate_presigned_post_url(file_key: str, file_type: str) -> dict:
    """Generates S3 Presigned POST payload or a local dummy mock payload."""
    if IS_LOCAL_DEMO:
        return {
            "url": f"http://localhost:8000/mock-s3-upload/{settings.S3_BUCKET_NAME}",
            "fields": {
                "key": file_key,
                "Content-Type": file_type,
                "AWSAccessKeyId": "mock-access-key",
                "policy": "mock-base64-policy-data",
                "signature": "mock-signature-hash"
            }
        }

    try:
        response = s3_client.generate_presigned_post(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_key,
            Fields={"Content-Type": file_type},
            Conditions=[
                {"Content-Type": file_type},
                ["content-length-range", 1, MAX_FILE_SIZE_BYTES]
            ],
            ExpiresIn=300
        )
        return response
    except BotoCoreError as err:
        raise MediaDatabaseException("Failed to communicate with S3 storage service.") from err


def get_s3_object_metadata(file_key: str) -> dict:
    """Fetches real-time metadata directly from S3 or simulates local object verification."""
    if IS_LOCAL_DEMO:
        # Simple local dummy validation check
        if file_key.startswith("invalid") or file_key.startswith("missing"):
            raise UploadConfirmationFailedException(
                "File object was not found in S3 storage. Upload may have failed or timed out."
            )
        return {
            "size_bytes": 1,  # Dummy 1 MB file size
            "mime_type": "image/png"
        }

    try:
        response = s3_client.head_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_key
        )
        return {
            "size_bytes": response["ContentLength"],
            "mime_type": response.get("ContentType", "")
        }
    except ClientError as err:
        raise UploadConfirmationFailedException(
            "File object was not found in S3 storage. Upload may have failed or timed out."
        ) from err


def generate_presigned_view_url(file_key: str, expires_in: int = 300) -> str:
    """Generates a short-lived presigned GET URL or a dummy local file URL."""
    if IS_LOCAL_DEMO:
        return f"http://localhost:8000/mock-media-view/{file_key}?token=mock-temp-token"

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": settings.S3_BUCKET_NAME,
                "Key": file_key,
            },
            ExpiresIn=expires_in
        )
        return url
    except BotoCoreError as err:
        raise MediaDatabaseException("Failed to generate temporary media viewing URL.") from err
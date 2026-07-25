import boto3
from botocore.exceptions import BotoCoreError ,ClientError
from src.core.config import settings  # Ensure AWS config is in your settings
from src.media.utils import MAX_FILE_SIZE_BYTES
from src.core.exceptions import MediaDatabaseException,UploadConfirmationFailedException

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def generate_presigned_post_url(file_key: str, file_type: str) -> dict:
    try:
        # Generates S3 Presigned POST payload with bucket-level security constraints
        response = s3_client.generate_presigned_post(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_key,
            Fields={"Content-Type": file_type},
            Conditions=[
                {"Content-Type": file_type},  # Require exact MIME type
                ["content-length-range", 1, MAX_FILE_SIZE_BYTES]  # Min 1 byte, Max 10 MB
            ],
            ExpiresIn=300  # Upload URL valid for 5 minutes
        )
        return response
    except BotoCoreError as err:
        raise MediaDatabaseException("Failed to communicate with S3 storage service.") from err


def get_s3_object_metadata(file_key: str) -> dict:
    """Fetches real-time metadata (ContentLength, ContentType) directly from S3."""
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
        # 404 or 403 error means the client never actually uploaded the file to S3
        raise UploadConfirmationFailedException(
            "File object was not found in S3 storage. Upload may have failed or timed out."
        ) from err

def generate_presigned_view_url(file_key: str, expires_in: int = 300) -> str:
    """Generates a short-lived presigned GET URL for viewing an S3 media object."""
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
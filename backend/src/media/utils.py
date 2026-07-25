from src.core.exceptions import (
    InvalidFileTypeException,
    FileTooLargeException
)

# Service validation before generating S3 URL
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB





def validate_upload_request(file_type: str, file_size_bytes: int):
    if file_type not in ALLOWED_MIME_TYPES:
        raise InvalidFileTypeException(
            f"Unsupported file type '{file_type}'. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    if file_size_bytes > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeException(
            f"File size exceeds maximum limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB."
        )
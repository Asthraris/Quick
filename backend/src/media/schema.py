from pydantic import BaseModel , ConfigDict,Field
from uuid import UUID
from datetime import datetime
from typing import Dict

#data sent to frontend
class mediaDetails(BaseModel):
    id : UUID
    uploader_id :UUID
    posted_at : datetime
    file_type :str
    file_size_bytes : int

    # Pydantic v2 syntax:
    model_config = ConfigDict(from_attributes=True)

class mediaMetaData(BaseModel):
    file_type :str
    file_size_bytes : int
    

# Presigned S3 Bucket Url with the Key of User that can access S3 using IAM auth
class PresignedViewResponse(BaseModel):
    url: str = Field(..., example="https://quick-media-bucket.s3.amazonaws.com/...")
    expires_in_seconds: int = Field(default=300, example=300)

class PresignedUploadResponse(BaseModel):
    media_id: UUID
    file_key: str
    upload_url: str
    fields: Dict[str, str]  # Required parameters to pass directly to S3 POST request


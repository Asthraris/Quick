from pydantic import BaseModel , ConfigDict
from uuid import UUID
from datetime import datetime

#data sent to frontend
class mediaDetails(BaseModel):
    id : UUID
    uploader_id :UUID
    posted_at : datetime
    file_type :str
    file_size_bytes : int

    # Pydantic v2 syntax:
    model_config = ConfigDict(from_attributes=True)


class MediaViewResponse(BaseModel):

    url: str


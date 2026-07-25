from fastapi import APIRouter,status , Depends , HTTPException
from src.core.database import get_db
from src.auth.dep import get_current_user
from sqlalchemy.orm import Session
from src.viewone.service import consume_and_log_image_view
from src.media.schema import PresignedUploadResponse, mediaMetaData , mediaDetails
from src.media import service 
from uuid import UUID

from src.core.exceptions import (
    ImageNotFoundException,
    ImageExpiredException,
    ImageAlreadyViewedException,
    MediaDatabaseException,
    CorruptedUploadException,
    UploadConfirmationFailedException,
    InvalidFileTypeException,
    FileTooLargeException
)
router = APIRouter(prefix="/media" , tags=["Resources"])

@router.post("/{im_id}/view",response_model=MediaURLResponse, status_code= status.HTTP_200_OK)
async def consumeAndLog(
    im_id : str ,
    curr_user = Depends(get_current_user),
    db :Session= Depends(get_db)
    ):
    try :
        im_url = await consume_and_log_image_view(
            im_id=im_id ,
            viewer_id=curr_user.id ,
            db = db
        )
        return MediaURLResponse(url=im_url , key = "S3-key")
    except ImageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ImageExpiredException as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=str(e)
        )

    except ImageAlreadyViewedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except MediaDatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed while recording view."
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the request."
        )


@router.post("/upload",response_model= PresignedUploadResponse ,status_code= status.HTTP_201_CREATED)
async def validateAndCreateMediaSignedUrl(
    meta_data :mediaMetaData,
    curr_user = Depends(get_current_user),
    db = Depends(get_db),
    ):
    try :
        return await service.uploadRequest(
            metadata= meta_data,
            uploaders_id= curr_user.id,
            db=db
        )
    except InvalidFileTypeException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except FileTooLargeException as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )

    except MediaDatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize upload request due to a database error.",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the presigned upload URL.",
        )

@router.post(
    "/{media_id}/confirm", 
    response_model=mediaDetails, 
    status_code=status.HTTP_200_OK
)
async def confirmUpload(
    media_id: UUID,
    curr_user = Depends(get_current_user),
    db = Depends(get_db)
    ):
    """Client calls this after successfully uploading binary data to S3."""
    try:
        activated_media = await service.confirm_media_upload(
            media_id=media_id,
            uploader_id=curr_user.id,
            db=db
        )
        return activated_media
    except ImageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except UploadConfirmationFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except CorruptedUploadException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

    except MediaDatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed during confirmation."
        )


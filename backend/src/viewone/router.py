from fastapi import APIRouter,status , Depends , HTTPException
from src.core.database import get_db
from src.auth.dep import get_current_user
from sqlalchemy.orm import Session
from src.viewone.service import consume_and_log_image_view

from src.media.schema import ImageViewResponse

from src.core.exceptions import (
    ImageNotFoundException,
    ImageExpiredException,
    ImageAlreadyViewedException,
    MediaDatabaseException,
)
router = APIRouter(prefix="/media" , tags=["Resources"])

@router.post("/{im_id}/view",response_model=ImageViewResponse, status_code= status.HTTP_200_OK)
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
        return ImageViewResponse(url=im_url)
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



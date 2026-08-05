from fastapi import APIRouter,status , Depends , HTTPException
from src.core.database import get_db
from src.auth.dep import get_current_user
from typing import List
from src.media import schema as mediaScm
from src.feed import service
from src.core.exceptions import (
    MediaDatabaseException,
    NoFriendsFoundException,
    EmptyFeedException,
)

router = APIRouter(tags=["Home"])

@router.get("/feed" , response_model=List[mediaScm.mediaDetails],status_code=status.HTTP_200_OK)
async def fetchEntireFeed(
    db = Depends(get_db),
    curr_user = Depends(get_current_user)
    ):
    try:
        # pydantic schema itself strips and converts model in to schema
        return await service.fetchEntireFeed(db= db , curr_user = curr_user)
    except (EmptyFeedException, NoFriendsFoundException):
        # Return an empty list so the frontend can render an empty feed state
        return []

    except MediaDatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load user feed due to a database error."
        )

    except Exception as e:
        # Fallback for unexpected system runtime errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"DEBUG ERROR: {type(e).__name__} - {str(e)}"
        )
    

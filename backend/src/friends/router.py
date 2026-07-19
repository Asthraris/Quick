from fastapi import APIRouter,status
from src.auth.schema import UserResponse

router = APIRouter(tags=["User"] , prefix="/user")

@router.get("/search" , response_model= UserResponse , status_code= status.HTTP_200_OK)
async def searchUser(q :str):

from fastapi import APIRouter,status,HTTPException

router = APIRouter(tags=["User"])

@router.post("/login")
async def login():
    return {
        "user":"id"
    }
from fastapi import FastAPI

#best way to include routers as also diff there work
from src.auth import router as auth_router
from src.health import router as health_router
from src.friends import router as friend_router


#Single line to initiatize  the app servlet
app = FastAPI()

# include router
app.include_router(auth_router.router)
app.include_router(health_router.router)
app.include_router(friend_router.router)





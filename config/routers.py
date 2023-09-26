from fastapi import APIRouter
from users.routers import router as users_routers
from auth.routers import router as auth_routers

router = APIRouter()
router.include_router(users_routers)
router.include_router(auth_routers)

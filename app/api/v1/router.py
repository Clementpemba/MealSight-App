from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    health,
    users,
    food_detection
)

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    food_detection.router,
    prefix="/food",
    tags=["Food Detection"]
)
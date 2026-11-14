from fastapi import APIRouter

from app.api.v1 import environment, farms, rotation

api_router = APIRouter()
api_router.include_router(farms.router, prefix="/farms", tags=["farms"])
api_router.include_router(environment.router, prefix="/environment", tags=["environment"])
api_router.include_router(rotation.router, prefix="/rotation", tags=["rotation"])

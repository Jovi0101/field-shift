from fastapi import APIRouter

from app.schemas.crop import CropRead
from app.services.crop_catalog import list_crops

router = APIRouter()


@router.get("", response_model=list[CropRead])
def get_crops() -> list[CropRead]:
    return list_crops()

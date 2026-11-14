from fastapi import APIRouter, HTTPException

from app.repositories.farm_repository import farm_repository
from app.schemas.rotation import RotationAnalyzeRequest, RotationAnalyzeResponse
from app.services import rotation_service

router = APIRouter()


@router.post("/analyze", response_model=RotationAnalyzeResponse)
def analyze_rotation(payload: RotationAnalyzeRequest) -> RotationAnalyzeResponse:
    farm = farm_repository.get(payload.farm_id)
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return rotation_service.analyze(farm, payload.priorities)

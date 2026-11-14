from fastapi import APIRouter, HTTPException, Query

from app.integrations.nasa.power_client import NasaPowerError
from app.schemas.climate import ClimateResponse
from app.services import climate_service

router = APIRouter()


@router.get("/climate", response_model=ClimateResponse)
def get_climate(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
) -> ClimateResponse:
    try:
        return climate_service.get_climate(latitude, longitude)
    except NasaPowerError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

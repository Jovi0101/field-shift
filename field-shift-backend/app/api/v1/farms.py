from fastapi import APIRouter, HTTPException, status

from app.repositories.farm_repository import farm_repository
from app.schemas.farm import FarmCreate, FarmRead

router = APIRouter()


@router.post("", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
def create_farm(payload: FarmCreate) -> FarmRead:
    return farm_repository.create(payload)


@router.get("", response_model=list[FarmRead])
def list_farms() -> list[FarmRead]:
    return farm_repository.list_all()


@router.get("/{farm_id}", response_model=FarmRead)
def get_farm(farm_id: str) -> FarmRead:
    farm = farm_repository.get(farm_id)
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

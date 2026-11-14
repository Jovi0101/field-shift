from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.farm import FarmModel
from schemas.farm_schema import FarmCreate, FarmResponse

router = APIRouter(prefix="/farms", tags=["Farms"])

@router.post("/", response_model=FarmResponse)
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    db_farm = FarmModel(
        name=farm.name,
        latitude=farm.latitude,
        longitude=farm.longitude,
        area_hectares=farm.area_hectares,
        soil_type=farm.soil_type
    )
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.get("/", response_model=list[FarmResponse])
def list_farms(db: Session = Depends(get_db)):
    return db.query(FarmModel).all()
from pydantic import BaseModel

class FarmCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    area_hectares: float
    soil_type: str

class FarmResponse(FarmCreate):
    id: int

    class Config:
        from_attributes = True
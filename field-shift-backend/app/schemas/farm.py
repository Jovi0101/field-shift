"""Contrato: cadastro da propriedade (Integrante 03 envia, Integrante 02 consome)."""
from enum import Enum

from pydantic import BaseModel, Field


class SoilType(str, Enum):
    clay = "clay"
    sandy = "sandy"
    loam = "loam"
    silt = "silt"


class FarmCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120, examples=["Farm Demo"])
    latitude: float = Field(ge=-90, le=90, examples=[-29.717])
    longitude: float = Field(ge=-180, le=180, examples=[-52.425])
    area_hectares: float = Field(gt=0, examples=[120])
    soil_type: SoilType = Field(examples=["clay"])
    irrigation: bool = False
    previous_crops: list[str] = Field(default_factory=list, examples=[["soybean", "corn"]])


class FarmRead(FarmCreate):
    id: str = Field(examples=["farm-001"])

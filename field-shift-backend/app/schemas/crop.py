"""Contrato do catálogo de culturas exibido pelo MVP."""
from pydantic import BaseModel


class CropRead(BaseModel):
    id: str
    name: str
    family: str
    season: str
    nitrogen_fixing: bool
    water_demand: str
    temperature_range_c: tuple[float, float]

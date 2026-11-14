"""Contrato: dados ambientais (Integrante 01 produz, 02 e 04 consomem).

Unidades:
- temperatura em °C (NASA POWER: T2M)
- precipitação em mm/dia (NASA POWER: PRECTOTCORR)
"""
from pydantic import BaseModel, Field


class Location(BaseModel):
    latitude: float
    longitude: float


class MonthlyClimate(BaseModel):
    month: str = Field(examples=["2024-01"], description="YYYY-MM")
    temperature_c: float
    precipitation_mm_day: float


class ClimateResponse(BaseModel):
    location: Location
    period: str = Field(examples=["2020-2024"])
    temperature_avg_c: float
    precipitation_avg_mm_day: float
    monthly: list[MonthlyClimate] = Field(default_factory=list)
    source: str = "NASA POWER"
    is_mock: bool = False

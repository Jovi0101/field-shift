"""Catálogo de culturas — dono: Integrante 02.

Valores ilustrativos para o MVP; revisar com fontes agronômicas antes da demo.
"""
from dataclasses import dataclass

from app.schemas.crop import CropRead


@dataclass(frozen=True)
class Crop:
    id: str
    name: str
    family: str  # famílias diferentes em sequência = melhor quebra de ciclo de pragas
    season: str  # "summer" | "winter"
    nitrogen_fixing: bool
    water_demand: str  # "low" | "medium" | "high"
    temp_min_c: float
    temp_max_c: float


CROPS: dict[str, Crop] = {
    c.id: c
    for c in [
        Crop("soybean", "Soybean", "Fabaceae", "summer", True, "medium", 20, 30),
        Crop("corn", "Corn", "Poaceae", "summer", False, "high", 18, 32),
        Crop("wheat", "Wheat", "Poaceae", "winter", False, "medium", 10, 24),
        Crop("oats", "Oats", "Poaceae", "winter", False, "low", 8, 22),
        Crop("bean", "Bean", "Fabaceae", "summer", True, "medium", 18, 28),
    ]
}


def list_crops() -> list[CropRead]:
    """Expõe o catálogo em um contrato estável, sem vazar a implementação interna."""
    return [
        CropRead(
            id=crop.id,
            name=crop.name,
            family=crop.family,
            season=crop.season,
            nitrogen_fixing=crop.nitrogen_fixing,
            water_demand=crop.water_demand,
            temperature_range_c=(crop.temp_min_c, crop.temp_max_c),
        )
        for crop in CROPS.values()
    ]

"""Catálogo de culturas — dono: Integrante 02.

Valores ilustrativos para o MVP; revisar com fontes agronômicas antes da demo.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Crop:
    id: str
    name_pt: str
    family: str  # famílias diferentes em sequência = melhor quebra de ciclo de pragas
    season: str  # "summer" | "winter"
    nitrogen_fixing: bool
    water_demand: str  # "low" | "medium" | "high"
    temp_min_c: float
    temp_max_c: float


CROPS: dict[str, Crop] = {
    c.id: c
    for c in [
        Crop("soybean", "Soja", "Fabaceae", "summer", True, "medium", 20, 30),
        Crop("corn", "Milho", "Poaceae", "summer", False, "high", 18, 32),
        Crop("wheat", "Trigo", "Poaceae", "winter", False, "medium", 10, 24),
        Crop("oats", "Aveia", "Poaceae", "winter", False, "low", 8, 22),
        Crop("bean", "Feijão", "Fabaceae", "summer", True, "medium", 18, 28),
    ]
}

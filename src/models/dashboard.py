from dataclasses import dataclass


@dataclass
class Indicator:
    name: str
    value: str
    unit: str
    help_text: str


@dataclass
class Strategy:
    name: str
    score: float
    rotation: str
    estimated_yield: float
    water_use: float
    soil_health: str
    justification: str
    risks: list[str]

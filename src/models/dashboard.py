from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Indicator:
    name: str
    value: str
    unit: str
    help_text: str


@dataclass
class RotationStrategy:
    """Estratégia no formato desenhado pelos componentes (vinda do backend ou do fallback)."""

    name: str
    score: float
    rotation: str
    criteria: dict[str, int] = field(default_factory=dict)
    benefits: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)


@dataclass
class DashboardData:
    indicators: list[Indicator]
    historical: pd.DataFrame | None
    strategies: list[RotationStrategy]
    is_demo: bool
    source_note: str
    history_caption: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class Strategy:
    """Formato antigo, usado apenas por src/data/sample_data.py (dados fictícios)."""

    name: str
    score: float
    rotation: str
    estimated_yield: float
    water_use: float
    soil_health: str
    justification: str
    risks: list[str]

"""Motor agronômico do MVP.

As regras são transparentes e deliberadamente simples: elas combinam as
prioridades informadas com características do solo, irrigação e histórico da
propriedade. Não substituem recomendação de um engenheiro agrônomo; servem
para validar o fluxo e deixar explícito por que uma estratégia ficou melhor.
"""
from dataclasses import dataclass

from app.schemas.farm import FarmRead
from app.schemas.rotation import Priorities, Recommendation, RotationAnalyzeResponse


CRITERIA_LABELS = {
    "soil_health": "Soil health",
    "water_efficiency": "Water efficiency",
    "climate_resilience": "Climate resilience",
    "diversification": "Diversification",
}


@dataclass(frozen=True)
class Strategy:
    name: str
    crops: list[str]
    criteria: dict[str, int]
    benefits: list[str]
    risks: list[str]


STRATEGIES = (
    Strategy(
        name="Winter cover",
        crops=["soybean", "oats", "corn"],
        criteria={"soil_health": 91, "water_efficiency": 70, "climate_resilience": 84, "diversification": 86},
        benefits=["Keeps the soil covered during winter", "Alternates Fabaceae and Poaceae families"],
        risks=["Corn requires close monitoring of water availability"],
    ),
    Strategy(
        name="Wheat income",
        crops=["soybean", "wheat", "soybean"],
        criteria={"soil_health": 72, "water_efficiency": 78, "climate_resilience": 73, "diversification": 56},
        benefits=["Creates a winter income option", "Lower water demand than corn"],
        risks=["Repeats soybean in the cycle and reduces family diversity"],
    ),
    Strategy(
        name="Bean diversification",
        crops=["corn", "oats", "bean"],
        criteria={"soil_health": 82, "water_efficiency": 68, "climate_resilience": 78, "diversification": 100},
        benefits=["Broadens crop diversity", "Includes a legume with biological nitrogen fixation"],
        risks=["Requires commercial and operational planning for beans"],
    ),
)


def _bounded(value: int) -> int:
    return max(0, min(100, value))


def _adjusted_criteria(strategy: Strategy, farm: FarmRead) -> dict[str, int]:
    """Ajustes pequenos deixam a resposta aderente ao perfil cadastrado."""
    criteria = dict(strategy.criteria)

    if farm.soil_type == "clay":
        criteria["soil_health"] += 3
    elif farm.soil_type == "sandy":
        criteria["water_efficiency"] -= 8
        criteria["climate_resilience"] -= 4
    elif farm.soil_type == "loam":
        criteria["soil_health"] += 1
        criteria["water_efficiency"] += 2

    if farm.irrigation:
        criteria["water_efficiency"] += 10
        criteria["climate_resilience"] += 4
    elif "corn" in strategy.crops:
        criteria["water_efficiency"] -= 5

    previous = [crop.lower().strip() for crop in farm.previous_crops]
    if previous and strategy.crops[0] == previous[-1]:
        criteria["diversification"] -= 4

    return {key: _bounded(value) for key, value in criteria.items()}


def _rationale(farm: FarmRead, priorities: Priorities, strategy: Strategy) -> list[str]:
    highest_priority = max(CRITERIA_LABELS, key=lambda key: getattr(priorities, key))
    details = [
        f"The top priority was {CRITERIA_LABELS[highest_priority].lower()} ({getattr(priorities, highest_priority)}%).",
        f"The reported soil is {farm.soil_type.value} and irrigation is {'available' if farm.irrigation else 'unavailable'}.",
    ]
    if farm.previous_crops:
        details.append(f"The crop history considered ends with {farm.previous_crops[-1]}.")
    if "oats" in strategy.crops:
        details.append("Oats were included as a winter cover crop.")
    return details


def _recommendation(strategy: Strategy, farm: FarmRead, priorities: Priorities) -> Recommendation:
    criteria = _adjusted_criteria(strategy, farm)
    weighted_score = sum(criteria[key] * getattr(priorities, key) for key in CRITERIA_LABELS) / 100
    risks = list(strategy.risks)
    if farm.soil_type == "sandy":
        risks.append("Sandy soil needs extra attention to water retention and organic matter")
    if not farm.irrigation and "corn" in strategy.crops:
        risks.append("Without irrigation, confirm the rainfall window before planting corn")

    return Recommendation(
        strategy=strategy.name,
        score=round(weighted_score),
        crops=strategy.crops,
        criteria=criteria,
        benefits=strategy.benefits,
        risks=risks,
        rationale=_rationale(farm, priorities, strategy),
    )


def analyze(farm: FarmRead, priorities: Priorities) -> RotationAnalyzeResponse:
    recommendations = [_recommendation(strategy, farm, priorities) for strategy in STRATEGIES]
    recommendations.sort(key=lambda recommendation: recommendation.score, reverse=True)
    return RotationAnalyzeResponse(farm_id=farm.id, recommendations=recommendations, is_mock=False)

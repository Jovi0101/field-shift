"""Motor agronômico do MVP.

As regras são transparentes e deliberadamente simples: elas combinam as
prioridades informadas com o clima do local (NASA POWER) e com características
do solo, irrigação e histórico da propriedade. Não substituem recomendação de
um engenheiro agrônomo; servem para validar o fluxo e deixar explícito por que
uma estratégia ficou melhor.

Como o clima entra na nota (critérios "water_efficiency" e "climate_resilience"):

1. Cada cultura é comparada com o clima da sua estação (meses dos últimos 5 anos completos):
   verão = out-mar e inverno = abr-set no hemisfério sul (invertido no norte).
   Sem meses daquela estação, usa a média anual.
   - chuva no ciclo = precipitação média da estação (mm/dia) x duração média do
     ciclo (dias); compara com a demanda hídrica do ciclo (mm, mínimo-máximo);
   - temperatura média da estação vs. faixa de temperatura da cultura.
2. A nota climática da estratégia é a média das notas das suas culturas.
3. A nota final do critério = metade da nota base da estratégia + metade da
   nota climática. Depois entram os ajustes por solo, irrigação e histórico.
"""
from dataclasses import dataclass

from app.data.crop_catalog import CATALOGO_CULTURAS
from app.integrations.nasa.power_client import NasaPowerError
from app.schemas.climate import ClimateResponse
from app.schemas.farm import FarmRead
from app.schemas.rotation import Priorities, Recommendation, RotationAnalyzeResponse
from app.services import climate_service
from app.services.crop_catalog import CROPS


CRITERIA_LABELS = {
    "soil_health": "Soil health",
    "water_efficiency": "Water efficiency",
    "climate_resilience": "Climate resilience",
    "diversification": "Diversification",
}

CLIMATE_CRITERIA = ("water_efficiency", "climate_resilience")


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


# --- Dados hídricos por cultura ---------------------------------------------

# ids das estratégias -> chaves de app/data/crop_catalog.py (CATALOGO_CULTURAS).
CATALOG_KEYS = {"soybean": "soja", "corn": "milho"}

# Trigo, aveia e feijão ainda não estão em CATALOGO_CULTURAS. Estimativas
# aproximadas (ordem de grandeza FAO) — REVISAR com fonte agronômica e, de
# preferência, mover para app/data/crop_catalog.py.
FALLBACK_WATER = {
    "wheat": {"ciclo_dias": {"minimo": 120, "maximo": 150}, "demanda_hidrica_mm": {"minimo": 450, "maximo": 650}},
    "oats": {"ciclo_dias": {"minimo": 110, "maximo": 130}, "demanda_hidrica_mm": {"minimo": 350, "maximo": 500}},
    "bean": {"ciclo_dias": {"minimo": 80, "maximo": 100}, "demanda_hidrica_mm": {"minimo": 300, "maximo": 500}},
}


@dataclass(frozen=True)
class CropWater:
    cycle_days: float
    demand_min_mm: float
    demand_max_mm: float


def _crop_water(crop_id: str) -> CropWater:
    entry = CATALOGO_CULTURAS.get(CATALOG_KEYS.get(crop_id, "")) or FALLBACK_WATER[crop_id]
    cycle = entry["ciclo_dias"]
    demand = entry["demanda_hidrica_mm"]
    return CropWater(
        cycle_days=(cycle["minimo"] + cycle["maximo"]) / 2,
        demand_min_mm=demand["minimo"],
        demand_max_mm=demand["maximo"],
    )


# --- Notas climáticas -------------------------------------------------------

SOUTH_SUMMER_MONTHS = {10, 11, 12, 1, 2, 3}


@dataclass(frozen=True)
class SeasonClimate:
    temperature_c: float
    precipitation_mm_day: float


def _season_climate(climate: ClimateResponse, season: str) -> SeasonClimate:
    """Média dos meses da estação da cultura; cai para a média anual se não houver meses."""
    southern = climate.location.latitude < 0
    months = []
    for m in climate.monthly:
        is_south_summer = int(m.month[5:7]) in SOUTH_SUMMER_MONTHS
        is_summer = is_south_summer if southern else not is_south_summer
        if is_summer == (season == "summer"):
            months.append(m)
    if not months:
        return SeasonClimate(climate.temperature_avg_c, climate.precipitation_avg_mm_day)
    return SeasonClimate(
        temperature_c=sum(m.temperature_c for m in months) / len(months),
        precipitation_mm_day=sum(m.precipitation_mm_day for m in months) / len(months),
    )


def _crop_climate(crop_id: str, climate: ClimateResponse) -> SeasonClimate:
    return _season_climate(climate, CROPS[crop_id].season)


def _water_score(crop_id: str, precipitation_mm_day: float) -> float:
    """100 se a chuva do ciclo cobre a demanda máxima; 75 na demanda mínima; cai linearmente abaixo dela."""
    water = _crop_water(crop_id)
    rain = precipitation_mm_day * water.cycle_days
    if rain >= water.demand_max_mm:
        return 100.0
    if rain >= water.demand_min_mm:
        return 75 + 25 * (rain - water.demand_min_mm) / (water.demand_max_mm - water.demand_min_mm)
    return 75 * rain / water.demand_min_mm


def _temperature_score(crop_id: str, temperature_c: float) -> float:
    """100 no centro da faixa da cultura, 75 nas bordas, -10 por °C fora da faixa."""
    crop = CROPS[crop_id]
    center = (crop.temp_min_c + crop.temp_max_c) / 2
    half_width = (crop.temp_max_c - crop.temp_min_c) / 2
    if crop.temp_min_c <= temperature_c <= crop.temp_max_c:
        return 100 - 25 * abs(temperature_c - center) / half_width
    outside = crop.temp_min_c - temperature_c if temperature_c < crop.temp_min_c else temperature_c - crop.temp_max_c
    return max(0.0, 75 - 10 * outside)


def _climate_scores(strategy: Strategy, climate: ClimateResponse) -> dict[str, float]:
    n = len(strategy.crops)
    local = {c: _crop_climate(c, climate) for c in strategy.crops}
    return {
        "water_efficiency": sum(_water_score(c, local[c].precipitation_mm_day) for c in strategy.crops) / n,
        "climate_resilience": sum(_temperature_score(c, local[c].temperature_c) for c in strategy.crops) / n,
    }


# --- Ajustes e montagem da recomendação ------------------------------------

def _bounded(value: float) -> int:
    return max(0, min(100, round(value)))


def _adjusted_criteria(strategy: Strategy, farm: FarmRead, climate: ClimateResponse | None) -> dict[str, int]:
    """Clima local (quando disponível) + ajustes pequenos pelo perfil cadastrado."""
    criteria: dict[str, float] = dict(strategy.criteria)

    if climate is not None:
        for key, climate_score in _climate_scores(strategy, climate).items():
            criteria[key] = (strategy.criteria[key] + climate_score) / 2

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


def _climate_sentence(climate: ClimateResponse | None, error: str | None) -> str:
    if climate is None:
        return (
            "NASA POWER climate data is currently unavailable"
            f"{f' ({error})' if error else ''}; water efficiency and climate resilience "
            "use the strategy's base scores."
        )
    origin = "demo data (mock mode)" if climate.is_mock else f"{climate.source}, {climate.period}"
    summer, winter = _season_climate(climate, "summer"), _season_climate(climate, "winter")
    return (
        f"Local climate ({origin}): average rainfall of {climate.precipitation_avg_mm_day * 365:.0f} mm/year "
        f"({climate.precipitation_avg_mm_day:.2f} mm/day) and average temperature of {climate.temperature_avg_c:.1f} °C "
        f"(summer {summer.temperature_c:.1f} °C and {summer.precipitation_mm_day:.2f} mm/day; "
        f"winter {winter.temperature_c:.1f} °C and {winter.precipitation_mm_day:.2f} mm/day)."
    )


def _climate_risks(strategy: Strategy, climate: ClimateResponse) -> list[str]:
    risks = []
    for crop_id in dict.fromkeys(strategy.crops):  # sem repetir culturas
        crop = CROPS[crop_id]
        water = _crop_water(crop_id)
        local = _crop_climate(crop_id, climate)
        rain = local.precipitation_mm_day * water.cycle_days
        if rain < water.demand_min_mm:
            risks.append(
                f"{crop.name}: estimated rainfall over the cycle ({rain:.0f} mm) is below the minimum water demand "
                f"({water.demand_min_mm:.0f} mm)"
            )
        if not crop.temp_min_c <= local.temperature_c <= crop.temp_max_c:
            risks.append(
                f"{crop.name}: average seasonal temperature ({local.temperature_c:.1f} °C) is outside the ideal "
                f"range ({crop.temp_min_c:.0f}–{crop.temp_max_c:.0f} °C)"
            )
    return risks


def _rationale(
    farm: FarmRead, priorities: Priorities, strategy: Strategy, climate: ClimateResponse | None, error: str | None
) -> list[str]:
    highest_priority = max(CRITERIA_LABELS, key=lambda key: getattr(priorities, key))
    details = [
        f"The top priority was {CRITERIA_LABELS[highest_priority].lower()} ({getattr(priorities, highest_priority)}%).",
        _climate_sentence(climate, error),
        f"The reported soil is {farm.soil_type.value} and irrigation is {'available' if farm.irrigation else 'unavailable'}.",
    ]
    if farm.previous_crops:
        details.append(f"The crop history considered ends with {farm.previous_crops[-1]}.")
    if "oats" in strategy.crops:
        details.append("Oats were included as a winter cover crop.")
    return details


def _recommendation(
    strategy: Strategy, farm: FarmRead, priorities: Priorities, climate: ClimateResponse | None, error: str | None
) -> Recommendation:
    criteria = _adjusted_criteria(strategy, farm, climate)
    weighted_score = sum(criteria[key] * getattr(priorities, key) for key in CRITERIA_LABELS) / 100
    risks = list(strategy.risks)
    if climate is not None:
        risks.extend(_climate_risks(strategy, climate))
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
        rationale=_rationale(farm, priorities, strategy, climate, error),
    )


def analyze(farm: FarmRead, priorities: Priorities) -> RotationAnalyzeResponse:
    climate: ClimateResponse | None = None
    error: str | None = None
    try:
        climate = climate_service.get_climate(farm.latitude, farm.longitude)
    except NasaPowerError as exc:
        # Sem clima a análise continua com as notas base; o motivo vai no rationale.
        error = str(exc)[:160]

    recommendations = [_recommendation(s, farm, priorities, climate, error) for s in STRATEGIES]
    recommendations.sort(key=lambda recommendation: recommendation.score, reverse=True)
    return RotationAnalyzeResponse(
        farm_id=farm.id,
        recommendations=recommendations,
        is_mock=bool(climate and climate.is_mock),
    )

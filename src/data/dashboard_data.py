"""Monta os dados do dashboard a partir do backend (real) ou do sample_data (fallback fictício)."""
import calendar

import pandas as pd

from src.data import api_client, sample_data
from src.models.dashboard import DashboardData, Indicator, RotationStrategy

MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _br(value: float, decimals: int = 1) -> str:
    return f"{value:,.{decimals}f}"


def monthly_climatology(climate: dict) -> pd.DataFrame:
    """Média por mês do calendário no período (ex.: todos os janeiros de 2020-2024).

    Precipitação convertida de mm/dia para mm/mês (x dias do mês).
    """
    rows = [
        {
            "month": int(m["month"][5:7]),
            "temp": m["temperature_c"],
            "rain_mm": m["precipitation_mm_day"] * calendar.monthrange(int(m["month"][:4]), int(m["month"][5:7]))[1],
        }
        for m in climate.get("monthly", [])
    ]
    if not rows:
        return pd.DataFrame(columns=["Month", "Temperature (°C)", "Precipitation (mm)"])
    grouped = pd.DataFrame(rows).groupby("month").mean().reindex(range(1, 13)).dropna()
    return pd.DataFrame(
        {
            "Month": [MONTH_LABELS[m - 1] for m in grouped.index],
            "Temperature (°C)": grouped["temp"].round(1).to_list(),
            "Precipitation (mm)": grouped["rain_mm"].round(0).to_list(),
        }
    )


def climate_indicators(climate: dict, history: pd.DataFrame) -> list[Indicator]:
    annual_rain = climate["precipitation_avg_mm_day"] * 365
    if history.empty:
        driest = "—"
    else:
        row = history.loc[history["Precipitation (mm)"].idxmin()]
        driest = f"{row['Month']} ({row['Precipitation (mm)']:.0f} mm)"
    source = "Demo" if climate.get("is_mock") else climate.get("source", "NASA POWER")
    return [
        Indicator("Average temperature", _br(climate["temperature_avg_c"]), "°C", f"Monthly average for {climate['period']}."),
        Indicator(
            "Average annual rainfall",
            _br(annual_rain, 0),
            "mm",
            f"{_br(climate['precipitation_avg_mm_day'], 2)} mm/day x 365, average for {climate['period']}.",
        ),
        Indicator("Driest month", driest, "", "Calendar month with the lowest average rainfall in the period."),
        Indicator("Climate source", source, "", f"Period {climate['period']}, {len(climate.get('monthly', []))} months."),
    ]


def _crop_names() -> dict[str, str]:
    try:
        return {crop["id"]: crop["name"] for crop in api_client.list_crops()}
    except (api_client.BackendUnavailable, api_client.BackendError):
        return {}


def load_real_dashboard(farm: dict, priorities: dict[str, int]) -> DashboardData:
    """Busca clima (NASA POWER via backend) e recomendações do motor de rotação.

    Lança api_client.BackendUnavailable se o backend cair no meio do caminho.
    """
    warnings: list[str] = []
    climate = None
    try:
        climate = api_client.get_climate(farm["latitude"], farm["longitude"])
    except api_client.BackendError as exc:
        warnings.append(f"Climate data is currently unavailable ({exc.detail}). Recommendations use the base scores.")

    analysis = api_client.analyze_rotation(farm["id"], priorities)
    names = _crop_names()
    strategies = [
        RotationStrategy(
            name=rec["strategy"],
            score=rec["score"],
            rotation=" → ".join(names.get(crop, crop) for crop in rec["crops"]),
            criteria=rec["criteria"],
            benefits=rec["benefits"],
            risks=rec["risks"],
            rationale=rec["rationale"],
        )
        for rec in analysis["recommendations"]
    ]

    if climate is not None:
        history = monthly_climatology(climate)
        indicators = climate_indicators(climate, history)
        is_demo = bool(climate.get("is_mock") or analysis.get("is_mock"))
        source_note = (
            "Climate in demo mode (USE_MOCK_CLIMATE=true in the backend)."
            if is_demo
            else f"Climate: NASA POWER {climate['period']} for ({farm['latitude']:.4f}, {farm['longitude']:.4f}). "
            "Recommendations: Field Shift backend rules engine."
        )
    else:
        history = None
        indicators = []
        is_demo = bool(analysis.get("is_mock"))
        source_note = "Recommendations from the Field Shift backend rules engine, without climate data."

    return DashboardData(
        indicators=indicators,
        historical=history,
        strategies=strategies,
        is_demo=is_demo,
        source_note=source_note,
        history_caption=(
            "Demo climate from the backend (mock mode)."
            if climate and climate.get("is_mock")
            else f"Average per calendar month, NASA POWER {climate['period']} (rainfall in mm/month)."
            if climate
            else ""
        ),
        warnings=warnings,
    )


def load_sample_dashboard() -> DashboardData:
    """Fallback com os dados fictícios de src/data/sample_data.py (backend fora do ar)."""
    strategies = [
        RotationStrategy(
            name=s.name,
            score=s.score,
            rotation=s.rotation,
            risks=list(s.risks),
            rationale=[s.justification],
        )
        for s in sample_data.get_strategies()
    ]
    return DashboardData(
        indicators=sample_data.get_indicators(),
        historical=sample_data.get_historical_data(),
        strategies=strategies,
        is_demo=True,
        source_note="FICTIONAL demo data (src/data/sample_data.py). Do not use for decisions.",
        history_caption="FICTIONAL demo series.",
    )
